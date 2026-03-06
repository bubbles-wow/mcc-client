from dataclasses import dataclass

from .pe_item import PeItem
from . import BaseEntity

@dataclass
class WaterFall(BaseEntity):
    tag: int
    campaign_id: int
    ret_list: list[PeItem]
    distribute_list: list[PeItem]
    is_end: bool = False