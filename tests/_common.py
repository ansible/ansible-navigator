""" common to all integration and unit tests """


def container_runtime_or_fail():
    """find a container runtime, prefer podman
    fail if neither available"""
    # pylint: disable=import-outside-toplevel
    import subprocess

    for runtime in ("podman", "docker"):
        try:
            subprocess.run([runtime, "-v"], check=False)
            return runtime
        except FileNotFoundError:
            pass
    raise Exception("container runtime required")
