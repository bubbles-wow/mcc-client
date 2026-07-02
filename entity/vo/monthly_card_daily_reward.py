from dataclasses import dataclass

from . import BaseEntity

@dataclass
class MonthlyCardDailyReward(BaseEntity):
    remaining_daily_rewards: int
    claimed_today: bool