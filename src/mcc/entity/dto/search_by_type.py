from dataclasses import dataclass

from . import BaseEntity

@dataclass
class SearchByType(BaseEntity):
    channel_id: int = 5
    length: int = 20
    first_type: int = "0"
    is_unofficial: bool = True
    offset: int = 0
    mod_second_type: str = "0"
    second_type: str = "0"
    asc_flag: bool = False
    sort_type: int = 0
    filter_type: int = 0