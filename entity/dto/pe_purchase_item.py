from dataclasses import dataclass, field
from typing import List, Any

from . import BaseEntity

@dataclass
class ExpertcommentInfo(BaseEntity):
    expertcomment_id: str = "0"
    video_url: str = "0"
    expert_id: str = "0"

@dataclass
class PePurchaseItem(BaseEntity):
    item_id: str
    cdk_code: str = ""
    expertcomment_info: ExpertcommentInfo = field(default_factory=ExpertcommentInfo)
    buy_path: str = "新版首页无主城_资源中心_推荐_ResourceDetailWindowV3_组件购买第二版"
    last_page: str = "资源中心首页_推荐-feed流"
    component_view: str = "资源中心首页_推荐-feed流"
    is_auto_buy: int = 0
    coupon_ids: List[Any] = field(default_factory=list)
    is_special_buy: int = 0

