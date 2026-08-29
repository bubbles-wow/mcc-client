from dataclasses import dataclass

from . import BaseEntity

@dataclass
class SearchSeasonMods(BaseEntity):
    length: int = 20
    offset: int = 0