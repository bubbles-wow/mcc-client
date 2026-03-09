from dataclasses import dataclass

from . import BaseEntity

@dataclass
class SearchByType(BaseEntity):
    """
    /pe-item/query/search-by-type/
    
    Arguments:
        first_type: enum [0: 全部, 1: 游戏地图, 2: 功能玩法, 3: 材质光影, 4: 皮肤]
        sort_type: enum [0: 综合排序/最新发布, 2: 按总获取量排序, 3: 按评分排序, 10: 最新发布, 11: 皮肤推荐, 16: 价格从高到低]
        filter_type: enum [0: 全部, 1: 免费, 2: 钻石, 3: 绿宝石]
        asc_flag: bool
    """
    channel_id: int = 5
    length: int = 20
    first_type: int = "0"
    is_unofficial: bool = True
    offset: int = 0
    mod_second_type: str = "0"
    second_type: str = "0"
    asc_flag: bool = False
    sort_type: int = 0
    filter_type: int = 0