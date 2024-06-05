from enum import Enum

from . import igdb
from .epic_store import Epic
from .steam_store import Steam
from .gog_store import GoG


class StorefrontEnum(Enum):
    ALL = 0
    STEAM = 1
    EPIC_GAMES = 2
    GOG = 3

    def __str__(self):
        return self.name


__all__ = [
    "igdb",
    "StorefrontEnum",
    "Epic",
    "Steam",
    "GoG",
]
