from nonebot.matcher import Matcher

from nonebot.exception import *


class ProcessException(Exception):
    
    """消息处理流程中异常的异常基类"""
    
    def __init__(self, message: str = "") -> None:
        
        self.message = message
        
        super().__init__(self.message)

def stop_propagation(matcher: Matcher) -> None:

    """终止事件处理流程

    参数:
    
        matcher: 当前事件的匹配器实例
    """
                
    matcher.stop_propagation()

    raise MatcherException("终止事件传播")