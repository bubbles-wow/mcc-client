import json

from dataclasses import dataclass
from typing import Optional

from . import BaseEntity

@dataclass
class SaData(BaseEntity):
    app_channel: str = "a50_sdk_cn"
    app_ver: Optional[str] = None
    core_num: Optional[str] = None
    cpu_digit: str = "0"
    cpu_hz: str = ""
    cpu_name: Optional[str] = None
    device_height: str = "1920"
    device_model: str = "Win32"
    device_width: str = "1080"
    disk: str = ""
    emulator: str = "0"
    first_udid: Optional[str] = None
    is_guest: str = "0"
    launcher_type: str = "PE_C++"
    mac_addr: str = "12-34-56-78-90-AB"
    network: str = ""
    os_name: str = "windows"
    os_ver: str = "10.0.26100"
    ram: str = "8192000000"
    rom: str = ""
    root: bool = False
    sdk_ver: str = "4.16.0"
    start_type: str = "default"
    udid: Optional[str] = None