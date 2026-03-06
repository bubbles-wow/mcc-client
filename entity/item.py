from dataclasses import dataclass
from typing import Any

from . import BaseEntity


@dataclass
class Item(BaseEntity):
    entity_id: str
    item_type: int
    name: str
    item_version: str
    developer_name: str
    master_type_id: int
    secondary_type_id: int
    brief_summary: str
    balance_grade: int
    available_scope: int
    review_status: int
    publish_time: int
    is_auth: bool
    goods_state: int
    resource_version: int
    game_status: int
    mod_id: int
    vip_only: bool
    season_begin: int
    season_number: int
    is_apollo: int
    rarity: int
    effect_mtypeid: int
    effect_stypeid: int
    rel_iid: str
    lobby_min_num: int
    lobby_max_num: int
    download_num: int
    like_num: int
    vanity_number: str
    normal_number: str
    is_current_season: bool
    is_has: bool
    t_expire: int
    is_refunding: int
    status: int
    network_tag: str
    dyeing_list: list[Any]
    dyeing_origin_iid: str
    dyeing_currency_num: int
    title_image_url: str
    vip_discount: int
    discount: int
    points: int
    diamonds: int
    expire_time: int