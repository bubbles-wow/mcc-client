from dataclasses import dataclass

from . import BaseEntity

@dataclass
class LoadItemsByDeveloperId(BaseEntity):
    developer_info_id: int
    channel_id: int = 5
    first_type: int = None
    sort_type: int = None
    offset: int = 0
    length: int = 12