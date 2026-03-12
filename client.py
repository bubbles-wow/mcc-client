import base64
import os
import json
import traceback
import uuid

from pathlib import Path
from logging import Logger
from requests import Response, Session
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional, Type

from .util import load_config_as_obj, http, CustomLogger, crypto, string
from .entity import (
    SaData, Sauth, Server, Response as X19Response, 
    Entity, User, Serverlist, ApiConfig, SessionConfig, X19Config,
    ClientConfig
)
from .service import auth
from .util import crypto, string

client_base_path = Path(__file__).parent

class Client:
    def __init__(self, session: Session, logger: Logger, server: Server, sa_data: SaData, sauth: Sauth, 
                 session_config: SessionConfig, api_config: ApiConfig, client_config: ClientConfig, 
                 force_relogin: bool = False) -> None:
        self.session = session
        self.logger = logger
        self.server = server
        self.api_config = api_config
        
        self.sa_data = SaData.from_any(sa_data)
        self.sauth = Sauth.from_any(sauth)
        
        self.pc_client = client_config.pc
        self.pe_client = client_config.pc_cocos
        if self.sa_data.os_name == "android":
            self.pe_client = client_config.android
        
        self.user_info: Optional[User] = None
        self.expires_at: Optional[datetime] = None
        
        self.session_config = session_config
        
        self.session_dir = session_config.path
        self.session_path = os.path.join(self.session_dir, session_config.file_name
                                         .format(server_env=server.server_env, server_code=server.server_code))
        self._load_session()
        self._update_serverlist()
        
        api_host_list = [
            self.server.serverlist.api_gateway_url,
            self.server.serverlist.dc_web_url,
            self.server.serverlist.web_server_url
        ]
        self.api_host = api_host_list[self.server.api_host_flag] \
            if 0 <= self.server.api_host_flag < len(api_host_list) \
            else self.server.serverlist.api_gateway_url
        del api_host_list
        
        self._refresh_session(force_relogin=force_relogin)
            
    def _refresh_session(self, force_relogin: bool = False):
        tz = timezone(timedelta(hours=self.session_config.timezone))
        if force_relogin or self.user_info is None or self.expires_at is None:
            self._login()
        elif datetime.now(tz) >= self.expires_at:
            self._check_login_result(auth.authentication_update(self))

    def _load_session(self):
        if not os.path.exists(self.session_path):
            return
            
        try:
            with open(self.session_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                if data.get("expires_at"):
                    dt = datetime.fromisoformat(data["expires_at"])
                    if dt.tzinfo is None:
                        tz = timezone(timedelta(hours=self.session_config.timezone))
                        dt = dt.replace(tzinfo=tz)
                    self.expires_at = dt
                
                if data.get("user_info"):
                    self.user_info = User.from_any(data["user_info"])
                
                if data.get("server"):
                    dyn = data["server"]
                    self.server.etag = dyn.get("etag", "")
                    self.server.last_modified = dyn.get("last_modified", "")
                    
                    if dyn.get("serverlist"):
                        self.server.serverlist = Serverlist.from_any(dyn["serverlist"])
                    
        except Exception as e:
            self.logger.error(130, f"Failed to load session from {self.session_path} (exception={e})")
            self.logger.error(130, traceback.format_)
            pass
        
    def _encrypt_body(self, body: bytes, encrypt_body_type: int) -> bytes:
        final_body = body
        if encrypt_body_type == 1:
            final_body = crypto.x19_http_encrypt(body)
        elif encrypt_body_type == 2:
            encrypted_body = crypto.x19_http_encrypt(body)
            final_body = encrypted_body.hex().encode('utf-8')
        elif encrypt_body_type == 3:
            final_body = crypto.g79_http_encrypt(body)
        elif encrypt_body_type == 4:
            encrypted_body = crypto.g79_http_encrypt(body)
            final_body = encrypted_body.hex().encode('utf-8')
        return final_body
    
    def _decrypt_body(self, body: bytes, encrypt_body_type: int = 0) -> bytes:
        final_body = body
        if encrypt_body_type == 1:
            final_body = crypto.x19_http_decrypt(body)
        elif encrypt_body_type == 2:
            encrypted_bytes = bytes.fromhex(body.decode('utf-8'))
            final_body = crypto.x19_http_decrypt(encrypted_bytes)
        elif encrypt_body_type == 3:
            final_body = crypto.g79_http_decrypt(body)
        elif encrypt_body_type == 4:
            encrypted_bytes = bytes.fromhex(body.decode('utf-8'))
            final_body = crypto.g79_http_decrypt(encrypted_bytes)
        return final_body
        
    def _data_verify(self, response: Response, encrypt_body_type: int = 0) -> bool:
        try:
            json_data = json.loads(self._decrypt_body(response.content, encrypt_body_type=encrypt_body_type).decode('utf-8'))
            if not isinstance(json_data, dict):
                self.logger.warning(140, (f"Response is not a JSON object! (url={response.url}, method={response.request.method},"
                                          f"response_text={response.text})"))
                return False
            status_code = json_data.get("code")
            if status_code != 0:
                self.logger.warning(141, (f"Unexpected response code! (url={response.url}, method={response.request.method}, "
                                          f"code={status_code}, message={json_data.get('message', 'None')}, response_body={json.dumps(json_data)})"))
                if status_code == 10 or status_code == 22:
                    self.logger.info(143, "Session expired, re-login required.")
                    self._login()
                return False
            return True
        except Exception as e:
            self.logger.error(142, f"Response verification failed! (url={response.url}, method={response.request.method}, exception={e})")
            self.logger.error(142, traceback.format_exc())
            return False
        
    def _get_request_headers(self, path: str, body: bytes = b"", extra_headers: Dict[str, str] = None) -> Dict[str, str]:
        return {
            "User-Agent": "WPFLauncher/0.0.0.0",
            "Content-Type": "application/json",
            "charset": "utf-8",
            "user-id": str(self.user_info.entity_id) if self.user_info else "",
            "user-token": crypto.compute_dynamic_token(path, body, self.user_info.token) if self.user_info else "",
            **(extra_headers or {})
        }

    def _update_user_info(self, new_user_info: User) -> None:
        tz = timezone(timedelta(hours=self.session_config.timezone))
        self.expires_at = datetime.now(tz) + timedelta(seconds=self.session_config.expired)
        self.user_info = new_user_info
        self._save_session()
        self.logger.info(150, f"Login successful. (user_id={self.user_info.entity_id}, expires_at={self.expires_at.isoformat()})")
        
    def _check_login_result(self, response: X19Response[User]) -> bool:
        if response is None or response.entity is None:
            self.logger.error(151, "Login failed: No user info in response.")
            return False
        self._update_user_info(response.entity)
        return True
        
    def is_logined(self) -> bool:
        return self.user_info is not None and self.expires_at is not None and datetime.now(timezone(timedelta(hours=self.session_config.timezone))) < self.expires_at
        
    def request(self, method: str, base_url: str, path: str, header: dict = None, body: bytes = b"", encrypt_body_type: int = 0, 
                           target_entity_type: Type[Entity] = None, **kwargs) -> X19Response | None:
        """encrypt_body_type: 0-no encryption, 1-x19encrypted, 2-x19encrypted hexadecimal, 
                            3-g79encrypted, 4-g79encrypted hexadecimal"""
        if string.is_empty(base_url):
            self.logger.error(101, f"Base URL is empty for API request! (method={method}, path={path})")
            return None
                            
        final_body = self._encrypt_body(body, encrypt_body_type=encrypt_body_type)
        self.logger.info(100, (f"Preparing request. (method={method}, url={base_url + path}, headers={header}, body={body.decode('utf-8', errors='replace')}, "
                               f"final_body_base64={base64.b64encode(final_body).decode()}, encrypt_body_type={encrypt_body_type})"))
            
        response = http.request(
            logger=self.logger,
            session=self.session,
            method=method,
            url=base_url + path,
            data=final_body,
            headers=self._get_request_headers(path, body, header),
            data_verify=lambda r: self._data_verify(r, encrypt_body_type=encrypt_body_type),
        )
        if response is None:
            return None
        response._content = self._decrypt_body(response.content, encrypt_body_type=encrypt_body_type)
        return X19Response.from_response(response, target_type=target_entity_type)
    
    def api_request(self, method: str, path: str, header: dict = None, body: bytes = b"", encrypt_body_type: int = 0, 
                           target_entity_type: Type[Entity] = None, **kwargs) -> X19Response[Entity] | None:
        self._refresh_session()
        return self.request(
            method=method,
            base_url=self.api_host,
            path=path,
            header=header,
            body=body,
            encrypt_body_type=encrypt_body_type,
            target_entity_type=target_entity_type,
            **kwargs
        )
    
    def get_user_id(self) -> Optional[str]:
        return str(self.user_info.entity_id) if self.user_info else None

    def _login(self):
        self.user_info = None
        self.expires_at = None
        if self.server.server_code == "x19":
            otp_response = auth.login_otp(self)
            if otp_response is not None and otp_response.entity is not None:
                self._check_login_result(auth.authentication_otp(self, otp_response.entity))
        elif self.server.server_code == "g79":
            self._check_login_result(auth.pe_authentication(self))
        else:
            self.logger.error(110, f"Unsupported server type for login: {self.server.server_code}")

    def _save_session(self):
        os.makedirs(self.session_dir, exist_ok=True)
        
        session_data = {
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "user_info": self.user_info.to_dict() if self.user_info else None,
            "server": {
                "etag": self.server.etag,
                "last_modified": self.server.last_modified,
                "serverlist": self.server.serverlist.to_dict() if self.server.serverlist else None
            }
        }
        
        with open(self.session_path, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=4)

    def _update_serverlist(self):
        headers = {}
        if self.server.etag:
            headers["If-None-Match"] = self.server.etag
        if self.server.last_modified:
            headers["If-Modified-Since"] = self.server.last_modified
        
        log_extra = f"server_env={self.server.server_env}, server_code={self.server.server_code}"
        try:
            response = self.session.get(self.server.serverlist_url, headers=headers, timeout=10)
            
            if response.status_code == 304:
                self.logger.info(120, f"Serverlist not modified. ({log_extra}, status_code=304).")
                return
            elif response.status_code == 200:
                self.logger.info(121, f"Serverlist updated. ({log_extra}, status_code=200).")
                data = response.json()
                
                data = string.convert_keys_to_snake(data)
                self.server.serverlist = Serverlist.from_any(data)
                
                self.server.etag = response.headers.get("ETag", "")
                self.server.last_modified = response.headers.get("Last-Modified", "")
                
                self._save_session()
            else:
                self.logger.warning(122, f"Failed to fetch serverlist! ({log_extra}, status_code={response.status_code})")
                
        except Exception as e:
            self.logger.error(123, f"Error updating serverlist: ({log_extra}, exception={e})")
            self.logger.error(123, traceback.format_exc())

class ClientManager:
    _clients: Dict[str, Client] = {}
    _config: Optional[X19Config] = None

    @classmethod
    def init(cls, config_path: Path = None) -> None:
        config_path = Path(__file__).parent / "config" / "x19.yaml" \
            if config_path is None else config_path
        _raw = load_config_as_obj(str(config_path))
        cls._config = X19Config.from_any(_raw)

    @classmethod
    def get_client(cls, server_env: str, server_code: str = "x19", 
                   session: Session = None, logger: CustomLogger = None, 
                   force_relogin: bool = False) -> Client:
        cache_key = f"{server_code}_{server_env}"
        if cache_key in cls._clients:
            return cls._clients[cache_key]
        
        if not cls._config:
            raise RuntimeError("X19ClientManager not initialized. Call init() first.")

        server_list = cls._config.server.get(server_code)
        if not server_list:
            return None
        
        server_detail = server_list.get(server_env)
        if not server_detail or not server_detail.serverlist_url:
            return None

        server = Server(
            serverlist_url=server_detail.serverlist_url,
            server_env=server_env,
            server_code=server_code,
            api_host_flag=server_detail.api_host_flag,
            etag="",
            last_modified="",
            serverlist=None
        )

        if session is None:
            session = Session()
        if logger is None:
            logger = CustomLogger("x19_client")
            
        client = Client(
            session=session,
            logger=logger,
            server=server,
            sa_data=cls._config.sa_data,
            sauth=cls._config.sauth,
            session_config=cls._config.session,
            api_config=server_detail.api_config,
            client_config=cls._config.client,
            force_relogin=force_relogin
        )
        if not client.is_logined():
            return None
        cls._clients[cache_key] = client
        return client

# initialize ClientManager
if os.getenv("DEBUG", "False").lower() == "true":
    ClientManager.init(client_base_path / "config" / "test_x19.yaml")
else:
    ClientManager.init()