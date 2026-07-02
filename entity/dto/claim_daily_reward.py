from dataclasses import dataclass

from . import BaseEntity

@dataclass
class ClaimDailyReward(BaseEntity):
    card_type: int
    platform: str