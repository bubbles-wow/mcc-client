from dataclasses import dataclass

from . import BaseEntity

@dataclass
class GetRankList(BaseEntity):
    rank_id: int
    channel_id: int = 5
    offset: int = 0