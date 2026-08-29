from dataclasses import dataclass

from . import BaseEntity

@dataclass
class GetMonthlyCardInfo(BaseEntity):
    platform: str
    card_types: list[int]