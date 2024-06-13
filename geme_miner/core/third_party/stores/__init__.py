from enum import Enum

from .epic import Epic
from .steam import Steam
from .gog import GoG
from .itchio import ItchIO


class StorefrontEnum(Enum):
    ALL = [Epic, Steam, ItchIO]
    RECOMMENDED = [Steam, Epic] # TODO: Remove
    STEAM = Steam
    EPIC = Epic
    #GOG = GoG
    ITCHIO = ItchIO

    def __str__(self):
        return self.name


__all__ = [
    "StorefrontEnum",
    "Epic",
    "Steam",
    "GoG",
    "ItchIO",
]
