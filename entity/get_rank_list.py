from dataclasses import dataclass

from . import BaseEntity

@dataclass
class GetRankList(BaseEntity):
    """
    /pe-item-rank/query/get-list
    
    Atguments:
        rank_id: enum [1: 热销榜, 2: 热玩榜, 3: 飙升榜, 4: 好评榜, 5: 整合包榜, 6: 付费榜]
    
    """
    channel_id: int = 5
    offset: int = 0
    rank_id: int = 1