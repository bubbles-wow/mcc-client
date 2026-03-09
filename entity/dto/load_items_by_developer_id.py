from dataclasses import dataclass

from . import BaseEntity

@dataclass
class LoadItemsByDeveloperId(BaseEntity):
    """
    /pe-developer-homepage/load_items_by_developer_info_id
    
    Atguments:
        developer_info_id: int
    
    """
    developer_info_id: int
    channel_id: int = 5
    offset: int = 0
    length: int = 12