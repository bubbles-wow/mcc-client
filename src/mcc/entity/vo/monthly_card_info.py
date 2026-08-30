from dataclasses import dataclass

from . import BaseEntity

@dataclass
class MonthlyCardInfoDetail(BaseEntity):
    card_type: int
    has_card: bool
    remaining_daily_rewards: int
    claimed_today: bool
    

@dataclass
class MonthlyCardInfo(BaseEntity):
    cards: list[MonthlyCardInfoDetail]