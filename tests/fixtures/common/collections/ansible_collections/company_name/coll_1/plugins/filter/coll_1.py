"""An ansible test filter plugin."""

from typing import Any


def filter_1() -> None:
    """Convert strings to Candlepin labels."""
    return


# ---- Ansible filters ----
class FilterModule:
    """Coll_1 filter."""

    def filters(self) -> dict[str, Any]:
        """Convert an arbitrary string to a valid Candlepin label.

        Returns:
            converted Candlepin label
        """
        return {
            "filter_1": filter_1,
        }
