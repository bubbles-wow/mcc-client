from typing import TYPE_CHECKING

from mcc.entity.dto.get_by_id import GetById
from mcc.entity.dto.get_by_urs import GetByUrs
from mcc.entity.vo.developer_homepage import DeveloperHomepage

from ..entity import Response
from ..entity.dto import SearchDeveloperByKeyword
from ..entity.vo import Developer

if TYPE_CHECKING:
    from ..client import Client

def search_by_keyword(client: 'Client', keyword: str, length: int = 30, offset: int = 0) -> Response[Developer]:
    body = SearchDeveloperByKeyword(keyword=keyword, length=length, offset=offset)
    return client.api_request(
        "POST",
        "/pe-developer-homepage/search_developer_by_keyword",
        body=body.to_json().encode(),
        target_entity_type=Developer
    )
    
def get_by_id(client: 'Client', id: str) -> Response[DeveloperHomepage]:
    body = GetById(id=id)
    return client.api_request(
        "POST",
        "/pe-developer-homepage/load_developer_homepage/get",
        body=body.to_json().encode(),
        target_entity_type=DeveloperHomepage
    )
    
def get_by_urs(client: 'Client', urs: str) -> Response[DeveloperHomepage]:
    body = GetByUrs(urs=urs)
    return client.api_request(
        "POST",
        "/pe-developer-homepage/load_developer_homepage_by_urs/get",
        body=body.to_json().encode(),
        target_entity_type=DeveloperHomepage
    )