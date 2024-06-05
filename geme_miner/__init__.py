from .__version__ import (
    __author__,
    __email__,
    __maintainer__,
    __copyright__,
    __license__,
    __version__,
)

from .core.third_party import (
    Steam,
    Epic,
    GoG,
)
from .core.normalize import (
    FormatTypeEnum,
    format_dict,
)

__all__ = [
    "__author__",
    "__email__",
    "__maintainer__",
    "__copyright__",
    "__license__",
    "__version__",
    "main",
    "Steam",
    "Epic",
    "GoG",
    "FormatTypeEnum",
    "format_dict",
]
