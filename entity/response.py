import requests

from dataclasses import dataclass
from typing import TypeVar, Generic, Type, Optional

from . import BaseEntity

Entity = TypeVar("Entity")

@dataclass
class Response(BaseEntity, Generic[Entity]):
    code: int = 0
    message: str = ""
    details: Optional[str] = None
    entity: Optional[Entity] = None
    entities: Optional[list[Entity]] = None
    total: Optional[int] = None
    summary_md5: Optional[str] = None

    @staticmethod
    def from_response(response: requests.Response, target_type: Type[Entity] = None) -> "Response[Entity]":
        try:
            data = response.json()
            # data = convert_keys_to_snake(data)
            res = Response.from_any(data)
            if target_type and isinstance(target_type, type) and issubclass(target_type, BaseEntity):
                if res.entity:
                    res.entity = target_type.from_any(res.entity)
                if res.entities:
                    res.entities = [target_type.from_any(item) for item in res.entities]
            return res
        except Exception:
            return None
