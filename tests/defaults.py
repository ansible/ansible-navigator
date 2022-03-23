"""Constants with default values used throughout the tests.
"""
import os


FIXTURES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "fixtures"))
FIXTURES_COLLECTION_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "fixtures", "common", "collections"),
)

# every attempt should be made for these images to share as many layers as possible
# or really small
DEFAULT_CONTAINER_IMAGE = "quay.io/ansible/creator-ee:v0.4.0"
SMALL_TEST_IMAGE = "quay.io/ansible/python-base:latest"
PULLABLE_IMAGE = "registry.hub.docker.com/library/alpine:latest"
