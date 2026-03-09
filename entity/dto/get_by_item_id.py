from dataclasses import dataclass

from . import BaseEntity

@dataclass
class GetByItemId(BaseEntity):
    item_id: str