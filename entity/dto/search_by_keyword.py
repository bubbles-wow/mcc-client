from dataclasses import dataclass, field

from . import BaseEntity

@dataclass
class SearchByKeyword(BaseEntity):
    official_skin: int = 0
    filter_domain_server_item: int = 0
    sort_type: int = 0
    first_type: int = 0
    second_type: list[int] = field(default_factory=list)
    mod_second_type: list[int] = field(default_factory=list)
    offset: int = 0
    keyword: str = ""
    price_type: int = 0
    init: int = 0
    channel_id: int = 5
    length: int = 24