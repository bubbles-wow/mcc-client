from typing import TYPE_CHECKING, List

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

def search_by_id_list(client: 'Client', item_ids: List[str]) -> Response[PeItem]:
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

def default_sort_water_fall(client: 'Client', item_ids: List[str] = [], 
                            first_type: int = 2, second_type: int = 0, 
                            price_type: int = 0) -> Response[WaterFall]:
    body = DefaultSortWaterFall(
        item_ids=item_ids,
        first_type=first_type,
        mod_second_type=second_type,
        price_type=price_type
    )
    return client.api_request(
        "POST",
        "/pe-item/default-sort-water-fall",
        body=body.to_json().encode(),
        target_entity_type=WaterFall
    )

def water_fall(client: 'Client', item_ids: List[str] = []) -> Response[WaterFall]:
    body = PeItemWaterFall(
        item_ids=item_ids,
        include_oversea_item=1
    )
    return client.api_request(
        "POST",
        "/pe-item/water_fall",
        body=body.to_json().encode(),
        target_entity_type=WaterFall
    )

def get_rank_list(client: 'Client', rank_id: int, offset: int = 0) -> Response[PeItem]:
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

def search_by_type(client: 'Client', first_type: int = 0, 
                   sort_type: int = 10, offset: int = 0, length: int = 20) -> Response[PeItem]:
    body = SearchByType(
        first_type=first_type,
        sort_type=sort_type,
        length=length,
        offset=offset,
        is_unofficial=False,
        asc_flag=False
    )
    return client.api_request(
        "POST",
        "/pe-item/query/search-by-type/",
        body=body.to_json().encode(),
        target_entity_type=PeItem
    )

def search_by_keyword(client: 'Client', keyword: str, first_type: int = 0, price_type: int = 0,
                      sort_type: int = 0, second_type: list[int] = [], mod_second_type: list[int] = [], 
                      offset: int = 0) -> Response[PeItem]:
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
    body = GetPeItemDetail(item_id=item_id)
    return client.api_request(
        "POST",
        "/pe-item-detail-v2",
        body=body.to_json().encode(),
        target_entity_type=PeItemDetail
    )

def load_items_by_developer_info_id(client: 'Client', developer_info_id: int, offset: int = 0) -> Response[PeItem]:
    body = LoadItemsByDeveloperId(
        developer_info_id=developer_info_id,
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

def get_encryption_key_list(client: 'Client', item_ids: List[str]) -> Response[EncryptKey]:
    body = GetEncryptKeyList(item_ids=item_ids)
    return client.api_request(
        "POST",
        "/pe-item/get-encryption-key-list",
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
