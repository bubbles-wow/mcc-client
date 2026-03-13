from dataclasses import dataclass

from . import BaseEntity

@dataclass
class DeveloperHomepage(BaseEntity):
    short_intro: str
    fellow_num: int
    developer_name: str
    back_image: str
    headimg: str
    grade: int
    current_class: int
    current_level: int
    class_name: str
    auth_tag: None
    is_fellow: int
    developer_info_id: int