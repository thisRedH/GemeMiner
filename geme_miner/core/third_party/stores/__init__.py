from enum import Enum

from .epic import Epic
from .steam import Steam
from .gog import GoG
from .itchio import ItchIO


class StorefrontEnum(Enum):
    ALL = 0
    STEAM = 1
    EPIC_GAMES = 2
    GOG = 3
    ITCHIO = 4

    def __str__(self):
        return self.name


__all__ = [
    "StorefrontEnum",
    "Epic",
    "Steam",
    "GoG",
    "ItchIO",
]
