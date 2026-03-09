from dataclasses import dataclass
from typing import Any, List

from . import BaseEntity

@dataclass
class PeItemWaterFall(BaseEntity):
    item_ids: list[str]
    include_oversea_item: int = 0
    channel_id: int = 5
    version: int = 3