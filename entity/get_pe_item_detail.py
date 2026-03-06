from dataclasses import dataclass

from . import BaseEntity

@dataclass
class GetPeItemDetail(BaseEntity):
    """
    /pe-item-detail-v2
    """
    item_id: str
    channel_id: int = 5
    need_record: int = 0