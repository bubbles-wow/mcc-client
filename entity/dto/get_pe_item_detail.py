from dataclasses import dataclass

from . import BaseEntity

@dataclass
class GetPeItemDetail(BaseEntity):
    item_id: str
    channel_id: int = 5
    need_record: int = 0
    source: int = 3