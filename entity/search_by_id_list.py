from dataclasses import dataclass

from . import BaseEntity

@dataclass
class SearchByIdList(BaseEntity):
    item_id_list: list[str]
    channel_id: int = 5
