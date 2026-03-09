from dataclasses import dataclass
from typing import Any, Union, Optional

from . import BaseEntity

@dataclass
class PerfParams(BaseEntity):
    mem_size: Union[float, str]
    fps_k: Union[float, str]
    jank_k: Union[float, str]
    loading_time: Union[float, str]

@dataclass
class RecInfo(BaseEntity):
    name: str
    rec_info_from: int

@dataclass
class RefundInfo(BaseEntity):
    pass

@dataclass
class ScoreTrendJSON(BaseEntity):
    visual: float
    creativity: float
    performance: float
    playability: float


@dataclass
class PeItem(BaseEntity):
    """
    Quick item for page view
    
    Arguments:
        item_id: str
        first_type: item type, enum [0: all, 1: world, 2: mod, 3: visual and texture]
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
    item_id: str
    first_type: int
    second_type: int
    pic_tag_state: int
    res_name: str
    res_size: int
    res_md5: str
    stars: float
    download_num: int
    week_download_num: int
    points: int
    diamond: int
    res_version: int
    is_item_time_limit: int
    item_remain_time: int
    buy_state: int
    goods_state: int
    status: int
    skin_body_type: int
    title_image_url: str
    title_image_version: int
    resource_packs_version: str
    behavior_packs_version: str
    lobby_tag: list[int]
    rel_iid: float
    is_competitive: int
    adv_obtain_num: int
    discount: int
    vip_discount: int
    is_vip_benefit: int
    pay_channel: str
    product_id: str
    is_recommend: int
    rec_info: RecInfo
    remark_num: int
    is_top: int
    is_joint: int
    sell_tags: list[Any]
    rebate_activity_id: int
    is_ea: int
    season_mod_id: int
    entity_id: str
    vip_only: bool
    season_begin: int
    rebate_max_num: int
    rebate_discount_num: int
    playing_uuid: str
    behaviour_uuid: str
    is_sync: int
    item_pack_iids: list[Any]
    performance_score: int
    playability_score: float
    creativity_score: float
    visual_score: float
    score_player_num: int
    performance_distribution: dict[str, int]
    playability_distribution: dict[str, int]
    creativity_distribution: dict[str, int]
    visual_distribution: dict[str, int]
    score_trend_json: Union[dict[str, ScoreTrendJSON], list[Any]]
    cur_num: int
    discount_end_time: int
    mod_version: str
    non_support_mod_versions: str
    rarity: int
    is_lottery_reward: bool
    is_persona: int
    lottery_id: int
    persona_mtypeid: int
    persona_stypeid: int
    suit_id: int
    dyeing: str
    t_buy: int
    t_expire: int
    activity_only: int
    developer_name: str
    developer_urs: str
    exchange_type: int
    is_wish: int
    refund_info: RefundInfo
    is_official_item: int
    pvp: bool
    demo_id: int
    vanity_number: str
    normal_number: int
    is_domain_server_item: int
    is_vertical_item: int
    perf_params: Optional[PerfParams]
    last_opr_time: int
    mod_second_type: int
    label_type_list: Optional[list[int]]
    rebate_tag: int
    is_distribute: bool
    reason_id: Optional[int]
    
