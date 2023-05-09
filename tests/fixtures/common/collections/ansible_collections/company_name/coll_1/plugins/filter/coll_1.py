"""An ansible test filter plugin."""


def filter_1():
    """Convert strings to Candlepin labels."""
    return


# ---- Ansible filters ----
class FilterModule:
    """Coll_1 filter."""

    def filters(self):
        """Convert an arbitrary string to a valid Candlepin label.

        :returns: converted Candlepin label
        """
        return {
            "filter_1": filter_1,
        }
