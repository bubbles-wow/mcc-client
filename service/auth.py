import uuid
from typing import TYPE_CHECKING

from mcc.entity.dto.login_otp import LoginOtp

from ..entity import User, Response
from ..entity.dto import LoginOtp, Authentication, PeAuthentication
from ..entity.vo import Otp
from ..util import crypto, string

if TYPE_CHECKING:
    from ..client import Client

def login_otp(client: 'Client') -> Response[Otp] | None:
    body = LoginOtp(sauth_json=client.sauth.to_json())
    config = client.api_config.login_otp
    return client.request(
        method="POST",
        base_url=getattr(client.server.serverlist, string.to_snake_case(config.host)) if config.host else client.server.serverlist.core_server_url,
        path=config.path if config.path else "/login-otp",
        body=body.to_json().encode(),
        encrypt_body_type=config.encrypt_body_type,
        target_entity_type=Otp
    )

def authentication_otp(client: 'Client', otp: Otp) -> Response[User] | None:
    if not otp:
        return
    client.sa_data.app_ver = client.client_config.version
    body = Authentication(
        sa_data=client.sa_data.to_json(),
        sauth_json=client.sauth.to_json(),
        otp_token=otp.otp_token,
        aid=otp.aid,
        version=client.client_config.to_dict()
    )
    config = client.api_config.authentication_otp
    return client.request(
        method="POST",
        base_url=getattr(client.server.serverlist, string.to_snake_case(config.host)) if config.host else client.server.serverlist.core_server_url,
        path=config.path if config.path else "/authentication-otp",
        body=body.to_json().encode(),
        encrypt_body_type=config.encrypt_body_type,
        target_entity_type=User
    )
    

def pe_authentication(client: 'Client') -> Response[User] | None:
    seed = str(uuid.uuid4())
    message = client.client_config.engine_version + client.client_config.engine_hash + \
        client.client_config.patch_version + client.client_config.patch_hash + \
            client.client_config.sign_hash + seed
    client.sa_data.app_ver = client.client_config.patch_version
    body = PeAuthentication(
        engine_version=client.client_config.engine_version,
        message=message,
        patch_version=client.client_config.patch_version,
        pay_channel=client.client_config.pay_channel,
        sa_data=client.sa_data.to_json(),
        sauth_json=client.sauth,
        seed=seed,
        sign=crypto.pe_auth_sign(message)
        # sign=crypto.pe_auth_sign_old(message, 2, 9)
    )
    config = client.api_config.pe_authentication
    return client.request(
        method="POST",
        base_url=getattr(client.server.serverlist, string.to_snake_case(config.host)) if config.host else client.server.serverlist.core_server_url,
        path=config.path if config.path else "/pe-authentication",
        body=body.to_json().encode(),
        encrypt_body_type=config.encrypt_body_type,
        target_entity_type=User
    )

def authentication_update(client: 'Client') -> Response[User] | None:
    if client.user_info is None:
        return
    config = client.api_config.authentication_update
    return client.request(
        method="POST",
        base_url=getattr(client.server.serverlist, string.to_snake_case(config.host)) if config.host else client.server.serverlist.core_server_url,
        path=config.path if config.path else "/authentication/update",
        body=client.user_info.to_json().encode(),
        encrypt_body_type=config.encrypt_body_type,
        target_entity_type=User
    )
