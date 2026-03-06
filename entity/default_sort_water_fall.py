from dataclasses import dataclass, field
from typing import Any, List

from . import BaseEntity

@dataclass
class DefaultSortWaterFall(BaseEntity):
    """
    /pe-item/query/search-by-type/
    
    Arguments:
        item_ids: 排除的id列表
        first_type: enum [0: 全部, 1: 游戏地图, 2: 功能玩法, 3: 材质光影, 4: 皮肤]
        mod_second_type: enum [201: 武器装备, 208: 大型玩法, 202: 物品道具, 203: 更多生物, 205: 辅助工具, 206: 建筑与家具, 207: 视觉美化, 204: 方块与群系]
        price_type: enum [0: 全部, 1: 免费, 2: 钻石, 3: 绿宝石]
        play_label_list: enum list [102: 冒险, 101: 动作, 103: 魔法, 105: 解谜, 106: 拟真, 107: 生存, 108: 养老种田]
        theme_label_list: enum list [201: 科幻, 202: 国风, 203: 现代, 204: 惊悚, 205: 搞怪, 206: 仙侠, 207: 西幻, 208: 流行文化, 209: 玩梗]
    """
    item_ids: list[Any] = field(default_factory=list)
    price_type: int = 0
    mod_second_type: int = 0
    channel_id: int = 5
    first_type: int = 2
    play_label_list: list[Any] = field(default_factory=list)
    theme_label_list: list[Any] = field(default_factory=list)