from dataclasses import dataclass

from . import BaseEntity

@dataclass
class Serverlist(BaseEntity):
    host_num: int = 0
    server_host_num: int = 0
    temp_server_stop: int = 0
    cdn_url: str = ""
    h5_version_url: str = ""
    seadra_url: str = ""
    home_server_url: str = ""
    home_server_gray_url: str = ""
    web_server_url: str = ""
    web_server_gray_url: str = ""
    core_server_url: str = ""
    core_server_gray_url: str = ""
    transfer_server_url: str = ""
    transfer_server_http_url: str = ""
    transfer_server_new_http_url: str = ""
    moment_url: str = ""
    forum_url: str = ""
    auth_server_url: str = ""
    chat_server_url: str = ""
    path_n_url: str = ""
    pe_path_n_url: str = ""
    path_n_ipv6_url: str = ""
    pe_path_n_ipv6_url: str = ""
    link_server_url: str = ""
    api_gateway_url: str = ""
    api_gateway_wei_xin_url: str = ""
    api_gateway_gray_url: str = ""
    community_host: str = ""
    welfare_url: str = ""
    dc_web_url: str = ""
    rental_transfer_url: str = ""
    mgb_sdk_url: str = ""