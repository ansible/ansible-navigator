from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Protocol  # python3.8+
else:
    Protocol = object
