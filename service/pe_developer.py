from typing import TYPE_CHECKING

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