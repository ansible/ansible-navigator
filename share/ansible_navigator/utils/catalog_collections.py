# cspell:ignore ftype, chksum
"""Catalog collections within the execution environment."""
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
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import TYPE_CHECKING, Dict
from typing import Generator
from typing import List
from typing import Tuple

import yaml

from ansible.utils.plugin_docs import get_docstring  # type: ignore
from yaml.error import YAMLError


try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader  # type: ignore

if TYPE_CHECKING:
    from ansible_navigator.utils.key_value_store import KeyValueStore
else:
    try:
        from key_value_store import KeyValueStore
    except ImportError:
        from ansible_navigator.utils.key_value_store import KeyValueStore


# pylint: enable=import-error

PROCESSES = (multiprocessing.cpu_count() - 1) or 1


class CollectionCatalog:
    """A collection cataloger."""

    def __init__(self, directories: List[Path]):
        """Initialize the collection cataloger.

        :param directories: A list of directories that may contain collections
        """
        self._directories: List[Path] = directories
        self._collections: OrderedDict[str, Dict] = OrderedDict()
        self._errors: List[Dict[str, str]] = []
        self._messages: List[str] = []

    def _catalog_plugins(self, collection: Dict) -> None:
        """Catalog the plugins within a collection.

        :param collection: Details describing the collection
        """
        file_checksums = {}

        file_manifest_file = collection.get("file_manifest_file", {}).get("name")
        if file_manifest_file:
            file_path = Path(collection["path"], file_manifest_file)
            if file_path.exists():
                with open(file=file_path, encoding="utf-8") as fh:
                    try:
                        loaded = json.load(fh)
                        file_checksums = {v["name"]: v for v in loaded["files"]}
                    except (JSONDecodeError, KeyError) as exc:
                        self._errors.append({"path": str(file_path), "error": str(exc)})

        exempt = ["action", "module_utils", "doc_fragments"]
        plugin_directory = Path(collection["path"], "plugins")
        if plugin_directory.is_dir():
            plugin_dirs = [
                plugin_dir
                for plugin_dir in plugin_directory.iterdir()
                if plugin_dir.is_dir() and plugin_dir.name not in exempt
            ]
            for plugin_dir in plugin_dirs:
                plugin_type = plugin_dir.name
                if plugin_type == "modules":
                    plugin_type = "module"
                filenames = plugin_dir.glob("**/*.py")
                self._process_plugin_dir(
                    plugin_type,
                    filenames,
                    file_checksums,
                    collection,
                )

    @staticmethod
    def _generate_checksum(file_path: Path, relative_path: Path) -> Dict:
        """Generate a standard checksum for a file.

        :param file_path: The path to the file to generate a checksum for
        :param relative_path: The relative path within the collection directory structure
        :returns: Details about the file, including the checksum
        """
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as fh:
            for byte_block in iter(lambda: fh.read(4096), b""):
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
        self,
        plugin_type: str,
        filenames: Generator[Path, None, None],
        file_checksums: Dict[str, Dict],
        collection: Dict,
    ) -> None:
        """Process each plugin within one plugin directory.

        :param plugin_type: The type of plugins
        :param filenames: The filenames of the plugins
        :param file_checksums: The checksums for the plugin files
        :param collection: The details of the collection
        """
        for filename in filenames:
            if str(filename).startswith("__"):
                continue

            relative_path = Path(filename).relative_to(collection["path"])
            checksum_dict = file_checksums.get(str(relative_path))
            if not checksum_dict:
                checksum_dict = self._generate_checksum(filename, relative_path)
            checksum = checksum_dict[f"chksum_{checksum_dict['chksum_type']}"]
            collection["plugin_checksums"][checksum] = {
                "path": str(relative_path),
                "type": plugin_type,
            }

    def _one_path(self, directory: Path) -> None:
        """Process the contents of an <...>/ansible_collections/ directory.

        :param directory: The path to collections directory to walk and load
        """
        for directory_path in directory.glob("*/*/"):
            manifest_file = directory_path / "MANIFEST.json"
            galaxy_file = directory_path / "galaxy.yml"
            collection = None
            if manifest_file.exists():
                with open(file=manifest_file, encoding="utf-8") as fh:
                    try:
                        collection = json.load(fh)
                        collection["meta_source"] = "MANIFEST.json"
                    except JSONDecodeError:
                        error = {
                            "path": str(manifest_file),
                            "error": "failed to load MANIFEST.json",
                        }
                        self._errors.append(error)
            elif galaxy_file.exists():
                with open(file=galaxy_file, encoding="utf-8") as fh:
                    try:
                        collection = {"collection_info": yaml.load(fh, Loader=SafeLoader)}
                        collection["meta_source"] = "galaxy.yml"
                    except YAMLError:
                        error = {
                            "path": str(galaxy_file),
                            "error": "failed to load galaxy.yml",
                        }
                        self._errors.append(error)
            if collection:
                collection_name = f"{collection['collection_info']['namespace']}"
                collection_name += f".{collection['collection_info']['name']}"
                collection["known_as"] = collection_name
                collection["plugins"] = []
                collection["plugin_checksums"] = {}
                collection["path"] = str(directory_path)

                runtime_file = directory_path / "meta" / "runtime.yml"
                collection["runtime"] = {}
                if runtime_file.exists():
                    with open(file=runtime_file, encoding="utf-8") as fh:
                        try:
                            collection["runtime"] = yaml.load(fh, Loader=SafeLoader)
                        except YAMLError as exc:
                            self._errors.append({"path": str(runtime_file), "error": str(exc)})

                self._collections[collection["path"]] = collection
            else:
                msg = (
                    f"collection path '{directory_path}' is ignored as it does not"
                    " have 'MANIFEST.json' and/or 'galaxy.yml' file(s)."
                )
                self._messages.append(msg)

    def _find_shadows(self) -> None:
        """Determine which collections are hidden by another installation of the same."""
        collection_list = list(self._collections.values())
        counts = Counter([collection["known_as"] for collection in collection_list])
        for idx, (collection_path, o_collection) in reversed(
            list(enumerate(self._collections.items())),
        ):
            self._collections[collection_path]["hidden_by"] = []
            if counts[o_collection["known_as"]] > 1:
                for i_collection in reversed(collection_list[0:idx]):
                    if i_collection["known_as"] == o_collection["known_as"]:
                        self._collections[collection_path]["hidden_by"].insert(
                            0,
                            i_collection["path"],
                        )

    def process_directories(self) -> Tuple[Dict, List]:
        """Process each parent directory.

        :returns: All collections found and any errors
        """
        for directory in self._directories:
            collection_directory = directory / "ansible_collections"
            if collection_directory.exists():
                self._one_path(collection_directory)
        for _collection_path, collection in self._collections.items():
            self._catalog_plugins(collection)
        self._find_shadows()
        return self._collections, self._errors


def worker(pending_queue: multiprocessing.Queue, completed_queue: multiprocessing.Queue) -> None:
    """Extract the documentation from a plugin, place in completed queue.

    :param pending_queue: A queue with plugins to process
    :param completed_queue: The queue in which extracted documentation will be placed
    """
    # pylint: disable=import-outside-toplevel

    # load the fragment_loader _after_ the path is set
    from ansible.plugins.loader import fragment_loader  # type: ignore

    while True:
        entry = pending_queue.get()
        if entry is None:
            break
        collection_name, checksum, plugin_path = entry

        try:
            (doc, examples, returndocs, metadata) = get_docstring(
                filename=str(plugin_path),
                fragment_loader=fragment_loader,
                collection_name=collection_name,
            )

        except Exception as exc:  # pylint: disable=broad-except
            err_message = f"{type(exc).__name__} (get_docstring): {str(exc)}"
            completed_queue.put(("error", (checksum, plugin_path, err_message)))
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
            completed_queue.put(("plugin", (checksum, json.dumps(q_message, default=str))))
        except JSONDecodeError as exc:
            err_message = f"{type(exc).__name__} (json_decode_doc): {str(exc)}"
            completed_queue.put(("error", (checksum, plugin_path, err_message)))


def identify_missing(collections: Dict, collection_cache: KeyValueStore) -> Tuple[set, List, int]:
    """Identify plugins missing from the cache.

    :param collections: All plugins found across all collections
    :param collection_cache: The key value interface to a sqlite database
    :returns: Handled and plugins missing from the cache, including a count of plugins
    """
    handled = set()
    missing = []
    plugin_count = 0
    for _collection_path, collection in collections.items():
        for checksum, details in collection["plugin_checksums"].items():
            plugin_count += 1
            if checksum not in handled:
                if checksum not in collection_cache:
                    missing.append(
                        (
                            collection["known_as"],
                            checksum,
                            Path(collection["path"], details["path"]),
                        ),
                    )
                handled.add(checksum)
    return handled, missing, plugin_count


def parse_args() -> Tuple[argparse.Namespace, List[Path]]:
    """Parse the arguments from the command line.

    :returns: The parsed arguments and all directories to search
    """
    parser = argparse.ArgumentParser(description="Catalog collections.")
    parser.add_argument(
        "-d",
        dest="dirs",
        nargs="+",
        help="search within the specified directories",
        default=current_collection_paths,
    )

    parser.add_argument("-a", dest="adjacent", help="prepended to dirs")
    parser.add_argument(
        "-c",
        dest="collection_cache_path",
        help="path to collection cache",
        required=True,
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
        realpath = Path(directory).resolve()
        if realpath not in resolved:
            resolved.append(realpath)

    return parsed_args, resolved


def retrieve_collections_paths() -> Dict:
    """Retrieve the currently set collection paths.

    :returns: Errors or the configured collection directories
    """
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
    collection_cache: KeyValueStore,
    errors: List,
    missing: List,
    stats: Dict,
) -> None:
    # pylint: disable=too-many-locals
    """Extract the docs from the plugins.

    :param collection_cache: The key value interface to a sqlite database
    :param errors: Previous errors encountered
    :param missing: Plugins missing from the collection cache
    :param stats: Statistics related to the collection cataloging process
    """
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
            checksum, plugin = message
            collection_cache[checksum] = plugin
            stats["cache_added_success"] += 1
        elif message_type == "error":
            checksum, plugin_path, error = message
            collection_cache[checksum] = json.dumps({"error": error})
            errors.append({"path": str(plugin_path), "error": error})
            stats["cache_added_errors"] += 1


def run_command(cmd: List) -> Dict:
    """Run a command using subprocess.

    :param cmd: The command to run, split
    :returns: Errors and the stdout from the command run
    """
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
    # pylint: disable=protected-access
    """Run the collection catalog process.

    :returns: The results from the completed collection cataloging process
    """
    stats = {}
    stats["cache_added_success"] = 0
    stats["cache_added_errors"] = 0

    cc_obj = CollectionCatalog(directories=parent_directories)
    collections, errors = cc_obj.process_directories()
    stats["collection_count"] = len(collections)

    collection_cache_path = Path(args.collection_cache_path).resolve().expanduser()
    # compatibility with py36, pass string to sqlite3.connect
    if sys.version_info >= (3, 7):
        collection_cache = KeyValueStore(collection_cache_path)
    else:
        collection_cache = KeyValueStore(str(collection_cache_path))

    handled, missing, plugin_count = identify_missing(collections, collection_cache)
    stats["plugin_count"] = plugin_count
    stats["unique plugins"] = len(handled)
    stats["processed"] = len(missing)

    if missing:
        retrieve_docs(collection_cache, errors, missing, stats)

    cached_checksums = collection_cache.keys()
    stats["cache_length"] = len(collection_cache.keys())

    for _collection_path, collection in collections.items():
        for no_doc in set(collection["plugin_checksums"].keys()) - set(cached_checksums):
            del collection["plugin_checksums"][no_doc]

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

    COLLECTION_SCAN_PATHS = ":".join(str(parent) for parent in parent_directories)
    os.environ["ANSIBLE_COLLECTIONS_PATHS"] = COLLECTION_SCAN_PATHS

    result = main()
    result["stats"]["duration"] = (datetime.now() - start_time).total_seconds()
    result["collection_scan_paths"] = COLLECTION_SCAN_PATHS
    print(json.dumps(result, default=str))
