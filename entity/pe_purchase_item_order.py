from dataclasses import dataclass

from . import BaseEntity

@dataclass
class PePurchaseItemOrder(BaseEntity):
    buy_type: int
    entity_id: str
    order_info: str