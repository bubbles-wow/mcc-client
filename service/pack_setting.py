from typing import TYPE_CHECKING

from ..entity.dto import GetBySettingName
from ..entity.vo.setting_value import SettingValue
from ..entity import Response

if TYPE_CHECKING:
    from ..client import Client

def get_for_mcstudio(client: 'Client', setting_name: str) -> Response[SettingValue]:
    body = GetBySettingName(setting_name=setting_name)
    return client.api_request(
        method="POST", 
        path="/interconn/web/pack-setting/get-for-mcstudio", 
        body=body.to_json().encode(),
        target_entity_type=SettingValue
    )