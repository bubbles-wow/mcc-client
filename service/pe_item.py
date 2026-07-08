from typing import TYPE_CHECKING

from ..entity import Response
from ..entity.dto import (
    SearchByIdList, GetRankList, SearchByType, SearchByKeyword, SearchSeasonMods, 
    DefaultSortWaterFall, PeItemWaterFall, GetPeItemDetail, LoadItemsByDeveloperId,
    GetByItemId, GetEncryptKeyList, PePurchaseItem
)
from ..entity.vo import (
    PeItem, WaterFall, PeItemDetail, DownloadInfo, EncryptKey, 
    BuyItemResult, PePurchaseItemOrder, PurchaseResult
)

if TYPE_CHECKING:
    from ..client import Client

def search_by_id_list(client: 'Client', item_ids: list[str]) -> Response[PeItem]:
    body = SearchByIdList(item_id_list=item_ids)
    return client.api_request(
        "POST",
        "/pe-item/query/search-by-id-list",
        body=body.to_json().encode(),
        target_entity_type=PeItem
    )

def search_season_mods(client: 'Client', length: int = 20, offset: int = 0) -> Response[PeItem]:
    body = SearchSeasonMods(length=length, offset=offset)
    return client.api_request(
        "POST",
        "/pe-season-mod/search-season-mods",
        body=body.to_json().encode(),
        target_entity_type=PeItem
    )

def default_sort_water_fall(client: 'Client', item_ids: list[str] = [], first_type: int = 2, mod_second_type: int = 0, 
                            price_type: int = 0, play_label_list: list[int] = [], theme_label_list: list[int] = []) -> Response[WaterFall]:
    """
    /pe-item/default-sort-water-fall
    
    Arguments:
        item_ids: 排除的id列表
        first_type: enum [0: 全部, 1: 游戏地图, 2: 功能玩法, 3: 材质光影, 4: 皮肤]
        mod_second_type: enum [201: 武器装备, 208: 大型玩法, 202: 物品道具, 203: 更多生物, 205: 辅助工具, 206: 建筑与家具, 207: 视觉美化, 204: 方块与群系]
        price_type: enum [0: 全部, 1: 免费, 2: 钻石, 3: 绿宝石]
        play_label_list: enum list [102: 冒险, 101: 动作, 103: 魔法, 105: 解谜, 106: 拟真, 107: 生存, 108: 养老种田]
        theme_label_list: enum list [201: 科幻, 202: 国风, 203: 现代, 204: 惊悚, 205: 搞怪, 206: 仙侠, 207: 西幻, 208: 流行文化, 209: 玩梗]
    """
    body = DefaultSortWaterFall(
        item_ids=item_ids,
        first_type=first_type,
        mod_second_type=mod_second_type,
        price_type=price_type,
        play_label_list=play_label_list,
        theme_label_list=theme_label_list
    )
    return client.api_request(
        "POST",
        "/pe-item/default-sort-water-fall",
        body=body.to_json().encode(),
        target_entity_type=WaterFall
    )

def water_fall(client: 'Client', item_ids: list[str] = [], include_oversea_item: int = 0) -> Response[WaterFall]:
    body = PeItemWaterFall(
        item_ids=item_ids,
        include_oversea_item=include_oversea_item
    )
    return client.api_request(
        "POST",
        "/pe-item/water_fall",
        body=body.to_json().encode(),
        target_entity_type=WaterFall
    )

def get_rank_list(client: 'Client', rank_id: int, offset: int = 0) -> Response[PeItem]:
    """
    /pe-item-rank/query/get-list
    
    Atguments:
        rank_id: enum [1: 热销榜, 2: 热玩榜, 3: 飙升榜, 4: 好评榜, 5: 整合包榜, 6: 付费榜]
        offset: item start offset, default 0
    """
    body = GetRankList(
        rank_id=rank_id,
        offset=offset
    )
    return client.api_request(
        "POST",
        "/pe-item-rank/query/get-list",
        body=body.to_json().encode(),
        target_entity_type=PeItem
    )

def search_by_type(client: 'Client', first_type: int = 0, second_type: int = 0, mod_second_type: int = 0, 
                   filter_type: int = 0, sort_type: int = 10, length: int = 20, offset: int = 0, 
                   is_unofficial: bool = False, asc_flag: bool = False) -> Response[PeItem]:
    """
    /pe-item/query/search-by-type/
    
    Arguments:
        first_type: enum [0: 全部, 1: 游戏地图, 2: 功能玩法, 3: 材质光影, 4: 皮肤]
        sort_type: enum [0: 综合排序/最新发布, 2: 按总获取量排序, 3: 按评分排序, 10: 最新发布, 11: 皮肤推荐, 16: 价格从高到低]
        filter_type: enum [0: 全部, 1: 免费, 2: 钻石, 3: 绿宝石]
        asc_flag: bool
    """
    body = SearchByType(
        first_type=first_type,
        second_type=second_type,
        mod_second_type=mod_second_type,
        filter_type=filter_type,
        sort_type=sort_type,
        length=length,
        offset=offset,
        is_unofficial=is_unofficial,
        asc_flag=asc_flag
    )
    return client.api_request(
        "POST",
        "/pe-item/query/search-by-type/",
        body=body.to_json().encode(),
        target_entity_type=PeItem
    )

def search_by_keyword(client: 'Client', keyword: str, first_type: int = 0, price_type: int = 0,
                      sort_type: int = 0, second_type: list[int] = [], mod_second_type: list[int] = [], 
                      filter_type: int = 0, offset: int = 0) -> Response[PeItem]:
    """
    /pe-item/query/search-by-keyword/

    Attributes:
        official_skin: 
        filter_domain_server_item: 是否支持realm（山头）
        sort_type: enum [0: 默认, 1: 价格从高到低, 2: 价格从低到高, 3: 获取量从高到低]
        first_type: enum [0: 全部, 1: 游戏地图, 2: 功能玩法, 3: 材质光影, 4: 皮肤, 5: 春节礼包, 6: 联机地图, 
            7: persona, 8: 组合包]
        second_type: only for first type in [1, 3]
            0: 全部, 
            for frst type 1, world
                1: 闯关解谜, 2: 角色扮演, 3: 策略对战, 4: 建筑大观, 5: 其他地图
            for first type 2, mod
                6: 玩法拓展, 7: 原创道具, 8: 生物改造, 9: 其他功能, 19: 特色组件, 
                20: 特色生物, 22: 一键生成
            for first type 3, visual and texture
                11: 精美材质, 12: 炫酷光影
            for first type 4, skin
                13: 原版风格, 14: 科幻风格, 15: 神话风格, 16: 其他皮肤, 17: , 18: 4D皮肤, 
        mod_second_type: for first type 2, mod
            201: 武器装备, 202: 物品道具, 203: 更多生物, 204: 方块与群系, 205: 辅助工具, 
            206: 建筑与家具, 207: 视觉美化, 208: 大型玩法, 209: 服主管理工具
        offset: page start offset, default 0
        keyword: text search word, default empty
        price_type: enum [0: 全部, 1: 免费, 2: 钻石, 3: 绿宝石]
        init: default 0
        channel_id: default 5
        length: page size, default 24
    """
    body = SearchByKeyword(
        keyword=keyword,
        price_type=price_type,
        sort_type=sort_type,
        first_type=first_type,
        second_type=second_type,
        mod_second_type=mod_second_type,
        offset=offset
    )
    return client.api_request(
        "POST",
        "/pe-item/query/search-by-keyword/",
        body=body.to_json().encode(),
        target_entity_type=PeItem
    )

def get_detail_v2(client: 'Client', item_id: str) -> Response[PeItemDetail]:
    """
    /pe-item-detail-v2
    
    Arguments:
        item_id: item id
    """
    body = GetPeItemDetail(item_id=item_id)
    return client.api_request(
        "POST",
        "/pe-item-detail-v2",
        body=body.to_json().encode(),
        target_entity_type=PeItemDetail
    )

def load_items_by_developer_info_id(client: 'Client', developer_info_id: int, length: int = 12, 
                                    offset: int = 0) -> Response[PeItem]:
    """
    /pe-developer-homepage/load_items_by_developer_info_id
    
    Atguments:
        developer_info_id: developer id
    
    """
    body = LoadItemsByDeveloperId(
        developer_info_id=developer_info_id,
        length=length,
        offset=offset
    )
    return client.api_request(
        "POST",
        "/pe-developer-homepage/load_items_by_developer_info_id",
        body=body.to_json().encode(),
        target_entity_type=PeItem
    )

def get_download_info(client: 'Client', item_id: str) -> Response[DownloadInfo]:
    body = GetByItemId(item_id=item_id)
    return client.api_request(
        "POST",
        "/pe-download-item/get-download-info",
        body=body.to_json().encode(),
        target_entity_type=DownloadInfo
    )

def get_encryption_key_list(client: 'Client', item_ids: list[str], device_id: str = "123456") -> Response[EncryptKey]:
    """
    /pe-item/get-encryption-key-list
    
    Attributes:
        device_id: str, default "123456"
        item_ids: list[str], list of item_id to get encrypt key
    """
    body = GetEncryptKeyList(item_ids=item_ids, device_id=device_id)
    return client.api_request(
        "POST",
        "/pe-item/get-encryption-key-list",
        body=body.to_json().encode(),
        encrypt_body_type=2,
        target_entity_type=EncryptKey
    )
    
def get_encryption_key_list_for_guests(client: 'Client', item_ids: list[str], device_id: str = "123456") -> Response[EncryptKey]:
    """
    /pe-item/get-encryption-key-list-for-guests
    
    Attributes:
        device_id: str, default "123456"
        item_ids: list[str], list of item_id to get encrypt key
    """
    body = GetEncryptKeyList(item_ids=item_ids, device_id=device_id)
    return client.core_api_request(
        "POST",
        "/pe-item/get-encryption-key-list-for-guests",
        body=body.to_json().encode(),
        encrypt_body_type=2,
        target_entity_type=EncryptKey
    )

def purchase_item(client: 'Client', item_id: str) -> Response[PePurchaseItemOrder]:
    body = PePurchaseItem(item_id=item_id)
    return client.api_request(
        "POST",
        "/pe-purchase-item/",
        body=body.to_json().encode(),
        target_entity_type=PePurchaseItemOrder
    )

def buy_item_result(client: 'Client', order_id: str) -> Response[PurchaseResult]:
    body = BuyItemResult(orderid=order_id)
    return client.api_request(
        "POST",
        "/buy-item-result",
        body=body.to_json().encode(),
        target_entity_type=PurchaseResult
    )
