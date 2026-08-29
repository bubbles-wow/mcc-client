from dataclasses import dataclass
from typing import Any, Union, Optional

from . import BaseEntity


@dataclass
class PeItemLobbyInfo(BaseEntity):
    """
    Quick item for page view
    
    Arguments:
        item_id: str
        first_type: item type, enum [0: all, 1: world, 2: mod, 3: visual and texture, 4: skin, 8: multi mods pack]
        second_type: int
        pic_tag_state: int
        res_name: name of the resource
        res_size: size of the resource content in bytes
        res_md5: md5 hash of the resource
        stars: the average rating of the item, float in [0, 5]
        download_num: total download number
        week_download_num: total download number in the past week
        points: the price using emerald
        diamond: the price using diamond
        vanity_number: the number of the item use for quick search, maybe empty
        normal_number: the number of the item use for quick search
        buy_state: enum [0: not bought, 1: bought]
        goods_state: enum [0: off sale, 1: on sale]
    """
    iid: str
    first_type: int
    second_type: int
    res_name: str
    status: int
    lobby_res_url: str
    lobby_manifest_version: list[str]
    playing_uuid: str
    behaviour_uuid: str
    has_mod: bool
    mod_version: str
    
