from dataclasses import dataclass
from typing import Any

from . import BaseEntity

@dataclass
class StarsData:
    score: float
    user_count: int

@dataclass
class PerfParams:
    vega_const1: int
    vega_const2: int
    vega_const3: int
    vega_const4: int
    crash_rate: float

@dataclass
class ScoreTrendJSON:
    visual: float
    creativity: float
    performance: int
    playability: float

@dataclass
class VideoInfo(BaseEntity):
    url: str
    size: int
    cover: str

@dataclass
class PeItemDetail(BaseEntity):
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
    lobby_tag: list[Any]
    rel_iid: int
    is_competitive: int
    adv_obtain_num: int
    discount: int
    vip_discount: int
    is_vip_benefit: int
    pay_channel: str
    product_id: str
    is_recommend: int
    rec_info: list[Any]
    remark_num: int
    is_top: int
    is_joint: int
    sell_tags: list[Any]
    rebate_activity_id: int
    is_ea: int
    season_mod_id: int
    entity_id: str
    refresh_time: int
    create_time: int
    info: str
    developer_name: str
    comment_count: int
    mod_format: int
    pic_url_list: list[str]
    video_info_list: list[VideoInfo]
    vip_only: bool
    season_begin: int
    discount_end_time: int
    mod_version: str
    non_support_mod_versions: str
    performance_score: int
    playability_score: float
    creativity_score: float
    visual_score: float
    score_player_num: int
    performance_distribution: dict[str, int]
    playability_distribution: dict[str, int]
    creativity_distribution: dict[str, int]
    visual_distribution: dict[str, int]
    score_trend_json: dict[str, ScoreTrendJSON]
    developer_id: int
    headimg: str
    is_sync: int
    rarity: int
    is_lottery_reward: bool
    lottery_id: int
    is_fellow: int
    fellow_num: int
    playing_uuid: str
    behaviour_uuid: str
    auth_tag: None
    effect_mtypeid: int
    effect_stypeid: int
    is_wish: int
    stars_distribution: list[Any]
    stars_status: int
    special_discount_activity: int
    developer_urs: str
    trial_ticket: list[Any]
    refund_info: Any
    is_official_item: int
    pvp: bool
    tags: list[Any]
    demo_id: int
    vanity_number: str
    normal_number: int
    mod_second_type: int
    label_type_list: list[int]
    is_domain_server_item: int
    is_vertical_item: int
    comp_list: list[Any]
    jelly_id: str
    item_remain_adv_num: int
    item_means_daily_remain_num: int
    item_means_daily_total_num: int
    item_watch_num: int
    is_downloaded: int
    is_developer: int
    is_lobby_collection: int
    b_has_mall: int
    activity_id: str
    card_sub_type: int
    benefit_item_create_time: int
    benefit_item_end_time: int
    union_developer_list: list[Any]
    is_shopping_cart: int
    item_pack_iids: list[str]
    resource_pack_iids: list[Any]
    recent_stars_data: StarsData
    pay_stars_data: StarsData
    pay_download_num: int
    is_maintain: int
    free_play_time: int
    act_free_play_time: int
    perf_params: PerfParams
    used_free_play_ticket: int
    ticket_free_play_time: int
    has_guide: int
