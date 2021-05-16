""" catalog collections
"""
import argparse
import hashlib
import json
import multiprocessing
import os
import re
import subprocess
import sys


from collections import Counter
from collections import OrderedDict
from datetime import datetime
from glob import glob
from json.decoder import JSONDecodeError
from typing import Dict
from typing import List
from typing import Tuple

from ansible.utils.plugin_docs import get_docstring  # type: ignore

import yaml
from yaml.error import YAMLError

try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader  # type: ignore

from key_value_store import KeyValueStore  # type: ignore


PROCESSES = (multiprocessing.cpu_count() - 1) or 1


class CollectionCatalog:
    # pylint: disable=too-few-public-methods
    """collection cataloger"""

    def __init__(self, directories: List[str]):
        self._directories = directories
        self._collections: OrderedDict[str, Dict] = OrderedDict()
        self._errors: List[Dict[str, str]] = []
        self._messages: List[str] = []

    def _catalog_plugins(self, collection: Dict) -> None:
        """catalog the plugins within a collection"""
        path = collection["path"]
        file_chksums = {}

        file_manifest_file = collection.get("file_manifest_file", {}).get("name")
        if file_manifest_file:
            fpath = f"{path}/{file_manifest_file}"
            if os.path.exists(fpath):
                with open(fpath) as read_file:
                    try:
                        loaded = json.load(read_file)
                        file_chksums = {v["name"]: v for v in loaded["files"]}
                    except (JSONDecodeError, KeyError) as exc:
                        self._errors.append({"path": fpath, "error": str(exc)})

        exempt = ["action", "module_utils", "doc_fragments"]
        plugin_directory = os.path.join(path, "plugins")
        if os.path.isdir(plugin_directory):
            plugin_dirs = [
                (f.name, f.path)
                for f in os.scandir(plugin_directory)
                if f.is_dir() and f.name not in exempt
            ]
            for plugin_type, path in plugin_dirs:
                if plugin_type == "modules":
                    plugin_type = "module"
                for (dirpath, _dirnames, filenames) in os.walk(path):
                    self._process_plugin_dir(
                        plugin_type, filenames, file_chksums, dirpath, collection
                    )

    @staticmethod
    def _generate_chksum(file_path: str, relative_path: str) -> Dict:
        """genrate a std checksum for a file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as fhand:
            for byte_block in iter(lambda: fhand.read(4096), b""):
                sha256_hash.update(byte_block)
        res = {
            "name": relative_path,
            "ftype": "file",
            "chksum_type": "sha256",
            "chksum_sha256": sha256_hash.hexdigest(),
            "format": 1,
        }
        return res

    def _process_plugin_dir(
        self, plugin_type: str, filenames: List, file_chksums: Dict, dirpath: str, collection: Dict
    ) -> None:
        # pylint: disable=too-many-arguments
        """process each plugin within one plugin directory"""
        for filename in filenames:
            file_path = f"{dirpath}/{filename}"
            relative_path = file_path.replace(collection["path"], "")
            _basename, extention = os.path.splitext(filename)
            if not filename.startswith("__") and extention == ".py":
                chksum_dict = file_chksums.get(relative_path)
                if not chksum_dict:
                    chksum_dict = self._generate_chksum(file_path, relative_path)
                chksum = chksum_dict[f"chksum_{chksum_dict['chksum_type']}"]
                collection["plugin_chksums"][chksum] = {"path": relative_path, "type": plugin_type}

    def _one_path(self, directory: str) -> None:
        """process the contents of an <...>/ansible_collections/ directory"""
        for directory_path in glob(f"{directory}/*/*/"):
            manifest_file = f"{directory_path}/MANIFEST.json"
            galaxy_file = f"{directory_path}/galaxy.yml"
            collection = None
            if os.path.exists(manifest_file):
                with open(manifest_file) as read_file:
                    try:
                        collection = json.load(read_file)
                        collection["meta_source"] = "MANIFEST.json"
                    except JSONDecodeError:
                        error = {
                            "path": os.path.dirname(manifest_file),
                            "error": "failed to load MANIFEST.json",
                        }
                        self._errors.append(error)
            elif os.path.exists(galaxy_file):
                with open(galaxy_file) as read_file:
                    try:
                        collection = {"collection_info": yaml.load(read_file, Loader=SafeLoader)}
                        collection["meta_source"] = "galaxy.yml"
                    except YAMLError:
                        error = {
                            "path": os.path.dirname(galaxy_file),
                            "error": "failed to load galaxy.yml",
                        }
                        self._errors.append(error)
            if collection:
                cname = f"{collection['collection_info']['namespace']}"
                cname += f".{collection['collection_info']['name']}"
                collection["known_as"] = cname
                collection["plugins"] = []
                collection["plugin_chksums"] = {}
                collection["path"] = directory_path

                runtime_file = f"{directory_path}/meta/runtime.yml"
                collection["runtime"] = {}
                if os.path.exists(runtime_file):
                    with open(runtime_file) as read_file:
                        try:
                            collection["runtime"] = yaml.load(read_file, Loader=SafeLoader)
                        except YAMLError as exc:
                            self._errors.append({"path": runtime_file, "error": str(exc)})

                self._collections[collection["path"]] = collection
            else:
                msg = (
                    f"collection path '{directory_path}' is ignored as it does not"
                    " have 'MANIFEST.json' and/or 'galaxy.yml' file(s)."
                )
                self._messages.append(msg)

    def _find_shadows(self) -> None:
        """for each collection, determin which other collections are hiding it"""
        collection_list = list(self._collections.values())
        counts = Counter([collection["known_as"] for collection in collection_list])
        for idx, (cpath, o_collection) in reversed(list(enumerate(self._collections.items()))):
            self._collections[cpath]["hidden_by"] = []
            if counts[o_collection["known_as"]] > 1:
                for i_collection in reversed(collection_list[0:idx]):
                    if i_collection["known_as"] == o_collection["known_as"]:
                        self._collections[cpath]["hidden_by"].insert(0, i_collection["path"])

    def process_directories(self) -> Tuple[Dict, List]:
        """process each parent directory"""
        for directory in self._directories:
            collection_directory = f"{directory}/ansible_collections"
            if os.path.exists(collection_directory):
                self._one_path(collection_directory)
        for _cpath, collection in self._collections.items():
            self._catalog_plugins(collection)
        self._find_shadows()
        return self._collections, self._errors


def worker(pending_queue: multiprocessing.Queue, completed_queue: multiprocessing.Queue) -> None:
    """extract a doc from a plugin, place in completed q"""
    # pylint: disable=ungrouped-imports
    # pylint: disable=import-outside-toplevel

    # load the fragment_loader _after_ the path is set
    from ansible.plugins.loader import fragment_loader  # type: ignore

    while True:
        entry = pending_queue.get()
        if entry is None:
            break
        collection_name, chksum, plugin_path = entry

        try:
            (doc, examples, returndocs, metadata) = get_docstring(
                filename=plugin_path,
                fragment_loader=fragment_loader,
                collection_name=collection_name,
            )

        except Exception as exc:  # pylint: disable=broad-except
            err_message = f"{type(exc).__name__} (get_docstring): {str(exc)}"
            completed_queue.put(("error", (chksum, plugin_path, err_message)))
            continue

        try:
            q_message = {
                "plugin": {
                    "doc": doc,
                    "examples": examples,
                    "returndocs": returndocs,
                    "metadata": metadata,
                },
                "timestamp": datetime.utcnow().isoformat(),
            }
            completed_queue.put(("plugin", (chksum, json.dumps(q_message, default=str))))
        except JSONDecodeError as exc:
            err_message = f"{type(exc).__name__} (json_decode_doc): {str(exc)}"
            completed_queue.put(("error", (chksum, plugin_path, err_message)))


def identify_missing(collections: Dict, collection_cache: KeyValueStore) -> Tuple[set, List, int]:
    """identify plugins missing from the cache"""
    handled = set()
    missing = []
    plugin_count = 0
    for _cpath, collection in collections.items():
        for chksum, details in collection["plugin_chksums"].items():
            plugin_count += 1
            if chksum not in handled:
                if chksum not in collection_cache:
                    missing.append(
                        (collection["known_as"], chksum, f"{collection['path']}{details['path']}")
                    )
                handled.add(chksum)
    return handled, missing, plugin_count


def parse_args():
    """parse the cli args"""
    parser = argparse.ArgumentParser(description="Catalog collections.")
    parser.add_argument(
        "-d",
        dest="dirs",
        nargs="+",
        help="search withing the specified directories",
        default=current_collection_paths,
    )

    parser.add_argument("-a", dest="adjacent", help="prepended to dirs")
    parser.add_argument(
        "-c", dest="collection_cache_path", help="path to collection cache", required=True
    )
    parsed_args = parser.parse_args()

    adjacent = vars(parsed_args).get("adjacent")
    if adjacent:
        directories = [adjacent] + parsed_args.dirs
    else:
        directories = parsed_args.dirs

    directories.extend(reversed(sys.path))

    resolved = []
    for directory in directories:
        realpath = os.path.realpath(directory)
        if realpath not in resolved:
            resolved.append(realpath)

    return parsed_args, resolved


def retrieve_collections_paths() -> Dict:
    """retrieve the currently ser collection paths"""
    cmd = ["ansible-config", "dump", "|", "grep", "COLLECTIONS_PATHS"]
    proc_out = run_command(cmd)
    if "error" in proc_out:
        return proc_out
    regex = re.compile(r"^(?P<variable>\S+)\((?P<source>.*)\)\s=\s(?P<current>.*)$")
    parsed = regex.match(proc_out["stdout"])
    if parsed:
        try:
            current = yaml.load(parsed.groupdict()["current"], Loader=SafeLoader)
            return {"result": current}
        except (YAMLError, KeyError) as exc:
            return {"error": str(exc)}
    return {"error": f"corrupt current collection path: {proc_out['stdout']}"}


def retrieve_docs(
    collection_cache: KeyValueStore, errors: List, missing: List, stats: Dict
) -> None:
    # pylint: disable=too-many-locals
    """extract the docs from the plugins"""
    pending_queue = multiprocessing.Manager().Queue()
    completed_queue = multiprocessing.Manager().Queue()
    processes = []
    for _proc in range(PROCESSES):
        proc = multiprocessing.Process(target=worker, args=(pending_queue, completed_queue))
        processes.append(proc)
        proc.start()

    for entry in missing:
        pending_queue.put(entry)
    for _proc in range(PROCESSES):
        pending_queue.put(None)
    for proc in processes:
        proc.join()

    while not completed_queue.empty():
        message_type, message = completed_queue.get()
        if message_type == "plugin":
            chksum, plugin = message
            collection_cache[chksum] = plugin
            stats["cache_added_success"] += 1
        elif message_type == "error":
            chksum, plugin_path, error = message
            collection_cache[chksum] = json.dumps({"error": error})
            errors.append({"path": plugin_path, "error": error})
            stats["cache_added_errors"] += 1


def run_command(cmd: List) -> Dict:
    """run a command"""
    try:
        proc_out = subprocess.run(
            " ".join(cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            universal_newlines=True,
            shell=True,
        )
        return {"stdout": proc_out.stdout}
    except subprocess.CalledProcessError as exc:
        return {"error": str(exc)}


def main() -> Dict:
    """main"""
    stats = {}
    stats["cache_added_success"] = 0
    stats["cache_added_errors"] = 0

    cc_obj = CollectionCatalog(directories=parent_directories)
    collections, errors = cc_obj.process_directories()
    stats["collection_count"] = len(collections)

    collection_cache_path = os.path.abspath(os.path.expanduser(args.collection_cache_path))
    collection_cache = KeyValueStore(collection_cache_path)

    handled, missing, plugin_count = identify_missing(collections, collection_cache)
    stats["plugin_count"] = plugin_count
    stats["unique plugins"] = len(handled)
    stats["processed"] = len(missing)

    if missing:
        retrieve_docs(collection_cache, errors, missing, stats)

    cached_chksums = collection_cache.keys()
    stats["cache_length"] = len(collection_cache.keys())

    for _cpath, collection in collections.items():
        for no_doc in set(collection["plugin_chksums"].keys()) - set(cached_chksums):
            del collection["plugin_chksums"][no_doc]

    collection_cache.close()
    return {
        "collections": collections,
        "errors": errors,
        "stats": stats,
        "messages": cc_obj._messages,
    }


if __name__ == "__main__":
    start_time = datetime.now()

    collection_paths = retrieve_collections_paths()
    if "error" in collection_paths:
        sys.exit(collection_paths["error"])
    else:
        current_collection_paths = collection_paths["result"]

    args, parent_directories = parse_args()

    collection_scan_paths = ":".join(parent_directories)
    os.environ["ANSIBLE_COLLECTIONS_PATHS"] = collection_scan_paths

    result = main()
    result["stats"]["duration"] = (datetime.now() - start_time).total_seconds()
    result["collection_scan_paths"] = collection_scan_paths
    print(json.dumps(result, default=str))
