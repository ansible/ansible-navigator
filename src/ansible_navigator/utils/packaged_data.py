"""Functionality related to the retrieval of packaged data files."""

from enum import Enum

from .compatibility import importlib_resources


class ImageEntry(Enum):
    """A mapping of ID to sequence within the image dockerfile."""

    DEFAULT_EE = 0
    SMALL_IMAGE = 1
    PULLABLE_IMAGE = 2

    def get(self, app_name: str) -> str:
        """Retrieve an image name from the packaged container file.

        :param app_name: The name of the application.
        :returns: The default execution environment image.
        """
        file_contents = retrieve_content(app_name=app_name, filename="images_dockerfile")
        from_line = (line for line in file_contents.splitlines() if self.name in line)

        image = next(from_line).split()[1]
        return image


def retrieve_content(app_name: str, filename: str) -> str:
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
