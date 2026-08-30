from dataclasses import dataclass

from . import BaseEntity

@dataclass
class Developer(BaseEntity):
    _id: str
    author_info: str
    headimg: str
    fellow_num: int
    developer_name: str
    level: int
    official_level: int
    current_class: int
    current_level: int
    developer_type: str
    developer_urs: str
    back_image: str
    official_recommend: int
    recommend_reason: str
    credit_score: int
    class_name: str