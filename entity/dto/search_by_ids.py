from dataclasses import dataclass

from . import BaseEntity

@dataclass
class SearchByIds(BaseEntity):
    entity_ids: list[str]
    with_price: int = 1
    with_title_image: int = 1
    channel_id: int = 11
    is_has: bool = True
