from dataclasses import dataclass

from . import BaseEntity

@dataclass
class SearchDeveloperByKeyword(BaseEntity):
    """
    /pe-developer-homepage/search_developer_by_keyword
    
    
    """
    keyword: str
    length: int = 30
    offset: int = 0