import os

FIXTURES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "fixtures"))
FIXTURES_COLLECTION_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "fixtures", "common", "collections")
)
DEFAULT_CONTAINER_IMAGE = "quay.io/ansible/ansible-runner:devel"
