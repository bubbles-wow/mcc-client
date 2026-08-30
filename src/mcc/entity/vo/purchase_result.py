from dataclasses import dataclass

from . import BaseEntity

@dataclass
class PurchaseResult(BaseEntity):
    entity_id: str
    item_id: str
    user_id: str
    purchase_time: int
    last_play_time: int
    total_play_time: int
    expire_time: str
    is_expired: bool
    is_item_time_limit: int
    item_remain_time: int