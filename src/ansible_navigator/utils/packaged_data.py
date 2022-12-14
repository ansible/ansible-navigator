"""Functionality related to the retrieval of packaged data files."""

from .compatibility import importlib_resources


def retrieve_content(filename: str, app_name: str = "ansible_navgiator") -> str:
    """Retrieve the content of a packaged data file.

    :param app_name: The name of the application.
    :param filename: The name of the file to retrieve.
    :returns: The content of the file.
    """
    data_directory = "data"
    package = f"{app_name}.{data_directory}"

    with importlib_resources.files(package).joinpath(filename).open("r", encoding="utf-8") as fh:
        content = fh.read()

    return content
