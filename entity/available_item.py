from dataclasses import dataclass

from . import BaseEntity


@dataclass
class AvailableItem(BaseEntity):
    item_type: int = 2
    master_type_id: int = 0
    secondary_type_id: int = 0
    sort_type: int = 2
    order: int = 0
    offset: int = 0
    length: int = 36
    is_has: bool = True
    year: int = 0
    is_sync: int = 0
    price_type: int = 0