from dataclasses import dataclass, field

from . import BaseEntity

@dataclass
class SearchByKeyword(BaseEntity):
    """
    /pe-item/query/search-by-keyword/

    Attributes:
        official_skin: 
        filter_domain_server_item: 是否支持realm（山头）
        sort_type: enum [0: 默认, 1: 价格从高到低, 2: 价格从低到高, 3: 获取量从高到低]
        first_type: enum [0: 全部, 1: 游戏地图, 2: 功能玩法, 3: 材质光影, 4: 皮肤, 5: 春节礼包, 6: 联机地图, 
            7: persona, 8: 组合包]
        second_type: only for first type in [1, 3]
            0: 全部, 
            for frst type 1, world
                1: 闯关解谜, 2: 角色扮演, 3: 策略对战, 4: 建筑大观, 5: 其他地图
            for first type 2, mod
                6: 玩法拓展, 7: 原创道具, 8: 生物改造, 9: 其他功能, 19: 特色组件, 
                20: 特色生物, 22: 一键生成
            for first type 3, visual and texture
                11: 精美材质, 12: 炫酷光影
            for first type 4, skin
                13: 原版风格, 14: 科幻风格, 15: 神话风格, 16: 其他皮肤, 17: , 18: 4D皮肤, 
        mod_second_type: for first type 2, mod
            201: 武器装备, 202: 物品道具, 203: 更多生物, 204: 方块与群系, 205: 辅助工具, 
            206: 建筑与家具, 207: 视觉美化, 208: 大型玩法, 209: 服主管理工具
        offset: page start offset, default 0
        keyword: text search word, default empty
        price_type: enum [0: 全部, 1: 免费, 2: 钻石, 3: 绿宝石]
        init: default 0
        channel_id: default 5
        length: page size, default 24
    """
    official_skin: int = 0
    filter_domain_server_item: int = 0
    sort_type: int = 0
    first_type: int = 0
    second_type: list[int] = field(default_factory=list)
    mod_second_type: list[int] = field(default_factory=list)
    offset: int = 0
    keyword: str = ""
    price_type: int = 0
    init: int = 0
    channel_id: int = 5
    length: int = 24