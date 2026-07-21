"""Unit tests for the images action."""

from copy import deepcopy

from ansible_navigator.actions.images import Action
from ansible_navigator.configuration_subsystem import NavigatorConfiguration


def test_collect_image_list_marks_container_variant_as_execution_environment(mocker) -> None:
    args = deepcopy(NavigatorConfiguration)
    args.entry("container_engine").value.current = "container"
    args.entry("execution_environment_image").value.current = "ghcr.io/example/demo:latest"

    mocker.patch(
        "ansible_navigator.actions.images.inspect_all",
        return_value=(
            [
                {
                    "repository": "ghcr.io/example/demo",
                    "tag": "latest",
                    "image_id": "sha256:abc",
                    "created": "today",
                    "size": "1 GB",
                    "inspect": {
                        "details": {
                            "variants": [
                                {
                                    "config": {
                                        "config": {
                                            "labels": {"ansible-execution-environment": "true"},
                                        },
                                    },
                                },
                            ],
                        },
                    },
                },
            ],
            "",
        ),
    )

    action = Action(args=args)
    action._collect_image_list()

    assert len(action._images.value) == 1
    assert action._images.value[0]["execution_environment"] is True
