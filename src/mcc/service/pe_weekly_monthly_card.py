from typing import TYPE_CHECKING, List

from ..entity import Response
from ..entity.dto import (ClaimDailyReward, GetMonthlyCardInfo)
from ..entity.vo import (MonthlyCardDailyReward, MonthlyCardInfo)

if TYPE_CHECKING:
    from ..client import Client
    
def get_info(client: 'Client', platform: str = "ad", card_types: list = [1, 2]):
    """
    /pe-weekly-monthly-card/get-info

    Arguments:
        platform: enum [ad: 安卓, ios: 苹果]
        card_types: list[int], enum [1: 周卡, 2: 月卡]
    """
    body = GetMonthlyCardInfo(
        card_types=card_types,
        platform=platform
    )
    return client.api_request(
        "POST",
        "/pe-weekly-monthly-card/get-info",
        body=body.to_json().encode(),
        target_entity_type=MonthlyCardInfo
    )
    
def claim_daily_reward(client: 'Client', card_type: int = 1, platform: str = "ad") -> Response[MonthlyCardDailyReward]:
    """
    /pe-weekly-monthly-card/claim-daily-reward

    Arguments:
        card_type: enum [1: 周卡, 2: 月卡]
        platform: enum [ad: 安卓, ios: 苹果]
    """
    body = ClaimDailyReward(
        card_type=card_type,
        platform=platform
    )
    return client.api_request(
        "POST",
        "/pe-weekly-monthly-card/claim-daily-reward",
        body=body.to_json().encode(),
        target_entity_type=MonthlyCardDailyReward
    )
    