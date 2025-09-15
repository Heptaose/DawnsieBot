from pathlib import Path

from nonebot.adapters.onebot.v11 import *


async def send_msg(*msg):

    """发送消息（支持文字、@用户、图片等）"""

    lst = []
    
    for i in msg:

        if i[0] == "at":

            lst.append(MessageSegment.at(i[1]))
        
        elif i[0] == "text":

            lst.append(MessageSegment.text(i[1]))
        
        elif i[0] == "image_path":

            lst.append(MessageSegment.image(i[1]))
        
        elif i[0] == "local_image_path":

            abs_path = Path(i[1]).absolute()

            lst.append(MessageSegment.image(f"file:///{abs_path}"))
        
        elif i[0] == "voice_path":

            lst.append(MessageSegment.record(i[1]))
        
        elif i[0] == "local_voice_path":

            abs_path = Path(i[1]).absolute()

            lst.append(MessageSegment.record(f"file:///{abs_path}"))
        
        elif i[0] == "video_path":

            lst.append(MessageSegment.video(i[1]))
        
        elif i[0] == "local_video_path":

            abs_path = Path(i[1]).absolute()

            lst.append(MessageSegment.video(f"file:///{abs_path}"))
    
    return Message(lst)