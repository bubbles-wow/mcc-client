from dataclasses import dataclass, field
from typing import Any, List

from . import BaseEntity

@dataclass
class DefaultSortWaterFall(BaseEntity):
    item_ids: list[Any] = field(default_factory=list)
    price_type: int = 0
    mod_second_type: int = 0
    channel_id: int = 5
    first_type: int = 2
    play_label_list: list[Any] = field(default_factory=list)
    theme_label_list: list[Any] = field(default_factory=list)