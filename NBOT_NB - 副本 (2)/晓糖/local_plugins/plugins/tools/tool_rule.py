from nonebot.adapters import *

from nonebot.adapters.onebot.v11 import *

from nonebot.adapters.onebot.v11 import helpers

from nonebot.rule import *


def in_group(group_list: list) -> callable[[Event], bool]:

    """判断事件是否在指定的群组列表中

    参数:
    
        group_list: 群组 ID 列表

    返回:
        
        callable: 判断事件是否在群组列表中的函数
    """

    def _(event: Event):

        if not isinstance(event, GroupMessageEvent):

            return False

        return event.group_id in group_list
    
    return _

def grammar_check(text: str, grammar: callable[[str], bool]) -> bool:

    """语法检查

    参数:
    
        text: 待检查文本

        grammar: 语法

    返回:
        
        bool: 是否符合语法
    """

    return grammar(text)