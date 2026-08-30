from dataclasses import dataclass

from . import BaseEntity

@dataclass
class BuyItemResult(BaseEntity):
    orderid: str
    buy_type: int = 0