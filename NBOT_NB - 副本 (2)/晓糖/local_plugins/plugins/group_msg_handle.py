# -*- coding: utf-8 -*-

"""依赖导入"""
from .tools import *

import nonebot as nb


"""数据初始化"""
DATABASE = {

    "global": DataBase(path = r"./database/DATABASE.json", group_list = [], admin_list = [], black_list = []),

    "main_id": DataBase(path = r"./database/MAIN_ID.json"),

    "group_list": {}

}

if len(DATABASE["global"].group_list):

    for _group_id in DATABASE["global"].group_list:

        DATABASE["group_list"][_group_id] = {

            "db": DataBase(path = rf"./database/group_list/{_group_id}/DATABASE.json", admin_list = [], user_list = {"id_list": []}, black_list = []),

            "ai": DataBase(path = rf"./database/group_list/{_group_id}/ai/DATABASE.yaml", post = "yaml", role = None, api_key = None)
        }


"""定义全局变量"""
global_msg_list = {}  # 全局消息列表

global_msg_notice_list = {} # 全局通知列表


"""注册事件响应器"""
# 根消息处理
content_root = nb.on_message(rule = to_me(), priority = 1, block = False)

# 全局消息内容接收
content = nb.on_message(rule = Rule(in_group(DATABASE["global"].group_list)), priority = 2, block = False)

# 全局通知内容接收
content_notice = nb.on_notice(priority = 2, block = False)

# 全局消息初步处理
content_handle = nb.on_message(rule = Rule(in_group(DATABASE["global"].group_list)), priority = 3, block = False)

# 全局通知初步处理
content_notice_handle = nb.on_notice(priority = 3, block=False)

# 全局消息自定义行为处理
content_custom_handle = nb.on_message(rule = Rule(in_group(DATABASE["global"].group_list)), priority = 4, block = False)

# 全局通知自定义行为处理
content_notice_custom_handle = nb.on_notice(priority = 4, block=False)

# 全局消息本地存储
content_save = nb.on_message(rule = Rule(in_group(DATABASE["global"].group_list)), priority = 5, block = True)

# 全局通知本地存储
content_notice_save = nb.on_notice(priority = 5, block = True)


"""事件处理"""
@content_root.handle()

async def _(bot: Bot, event: MessageEvent, state: T_State, matcher: Matcher) -> None:

    message = event.get_message().extract_plain_text()

    if message == "启动" and event.user_id == DATABASE["main_id"].super_id:

        if event.group_id in DATABASE["global"].group_list:

            await content_root.send(await send_msg(["text", "BOT已存在, 请勿重复部署\n如有疑问请联系机器人管理者"], ["at", DATABASE["main_id"].super_id]))

            stop_propagation(matcher)

        DATABASE["global"].redata("group_list", event.group_id)

        DATABASE["group_list"][event.group_id] = {
        
            "db": DataBase(path = rf"./database/group_list/{event.group_id}/DATABASE.json", admin_list = [], user_list = {"id_list": []}, black_list = []),
        
            "ai": DataBase(path = rf"./database/group_list/{event.group_id}/ai/DATABASE.yaml", post = "yaml", role = None, api_key = None)
        
        }

        DATABASE["group_list"][event.group_id]["db"].save()

        DATABASE["group_list"][event.group_id]["ai"].save()

        await content_root.send(await send_msg(["text", "BOT部署成功, 请前往设置该群机器人管理员列表及AI角色等信息\n如有疑问请联系机器人管理者"], ["at", DATABASE["main_id"].super_id]))

        stop_propagation(matcher)

@content.handle()

async def _(bot:Bot, event: MessageEvent, state: T_State, matcher: Matcher):

    try:

        if DATABASE["group_list"][event.group_id]["db"].redata("user_list")["id_list"] == []:

            member_list = await bot.call_api("get_group_member_list", group_id = event.group_id)

            qq_numbers = [str(member["user_id"]) for member in member_list]

            DATABASE["group_list"][event.group_id]["db"].redata("user_list")["id_list"] = qq_numbers

        if event.user_id in DATABASE["group_list"][event.group_id]["db"].redata("black_list") or event.user_id in DATABASE["global"].redata("black_list"):

            stop_propagation(matcher)

        global_msg = {"msg_type": [], "user_id": event.user_id, "msg": ""}

        message = event.get_message()

        print(f"\n\n\nmessage: {message}\n\n\n")

        for segment in message:

            if segment.type == "text":

                global_msg["msg_type"].append("text_msg")
           
                global_msg["text"] = [segment.data["text"]] if "text" not in global_msg else global_msg["text"] + [segment.data["text"]]

                global_msg["msg"] += segment.data["text"]

            elif segment.type == "at":

                global_msg["msg_type"].append("at_msg")

                global_msg["at_id"] = [segment.data["qq"]] if "at_id" not in global_msg else global_msg["at_id"] + [segment.data["qq"]]

                global_msg["msg"] += f"<at: {segment.data['qq']}>"

            elif segment.type == "image":

                global_msg["msg_type"].append("image_msg")
                
                global_msg["image_url"] = [segment.data["url"]] if "image_url" not in global_msg else global_msg["image_url"] + [segment.data["url"]]

                global_msg["msg"] += f"<image: {segment.data['url']}>"
            
            elif segment.type == "record":

                global_msg["msg_type"].append("record_msg")
                
                global_msg["record_url"] = [segment.data["url"]] if "record_url" not in global_msg else global_msg["record_url"] + [segment.data["url"]]

                global_msg["msg"] += f"<record: {segment.data['url']}>"
            
            elif segment.type == "video":

                global_msg["msg_type"].append("video_msg")
                
                global_msg["video_url"] = [segment.data["url"]] if "video_url" not in global_msg else global_msg["video_url"] + [segment.data["url"]]

                global_msg["msg"] += f"<video: {segment.data['url']}>"
            
            elif segment.type == "share":

                global_msg["msg_type"].append("share_msg")
                
                global_msg["share_url"] = [segment.data["url"]] if "share_url" not in global_msg else global_msg["share_url"] + [segment.data["url"]]

                global_msg["title"] = [segment.data["title"]] if "title" not in global_msg else global_msg["title"] + [segment.data["title"]]

                global_msg["msg"] += f"<share: {segment.data['url']}>"

            elif segment.type == "json":

                global_msg["msg_type"].append("json_msg")
                
                global_msg["json_url"] = [segment.data["data"]] if "json_url" not in global_msg else global_msg["json_url"] + [segment.data["data"]]

                global_msg["msg"] += f"<json: {segment.data['data']}>"
            
            elif segment.type == "xml":

                global_msg["msg_type"].append("xml_msg")
                
                global_msg["xml_url"] = [segment.data["data"]] if "xml_url" not in global_msg else global_msg["xml_url"] + [segment.data["data"]]

                global_msg["msg"] += f"<xml: {segment.data['data']}>"

        print(f"\n\n\nglobal_msg: {global_msg}\n\n\n")

        if event.group_id not in global_msg_list:

            global_msg_list[event.group_id] = []

        global_msg_list[event.group_id].append(global_msg)

    except MatcherException as e:

        print(f"\n\n当前事件正常结束, 原文: {e}\n")

    except ProcessException as e:

        print(f"\n\n当前事件(消息接收)处理异常结束, 原文: {e}\n")

        await content.finish(f"消息接收时发生了一些错误, 原文: {e}")

@content_notice.handle()

async def _(event: Union[
    
    PokeNotifyEvent,

    GroupIncreaseNoticeEvent,

    GroupDecreaseNoticeEvent
    
    ],
    
    matcher: Matcher):
        
    try:

        if DATABASE["group_list"][event.group_id]["db"].redata("user_list")["id_list"] == []:

            member_list = await bot.call_api("get_group_member_list", group_id = event.group_id)

            qq_numbers = [str(member["user_id"]) for member in member_list]

            DATABASE["group_list"][event.group_id]["db"].redata("user_list")["id_list"] = qq_numbers

        if event.user_id in DATABASE["group_list"][event.group_id]["db"].redata("black_list") or event.user_id in DATABASE["global"].redata("black_list"):

            stop_propagation(matcher)
    
        global_msg = {

            "msg_type": [],

            "user_id": event.user_id,

            "group_id": event.group_id
    
        }
    
        if isinstance(event, PokeNotifyEvent): # 戳一戳

            global_msg["msg_type"] = "poke_msg"

            global_msg["target_id"] = event.target_id
    
        elif isinstance(event, GroupIncreaseNoticeEvent): # 入群

            global_msg["msg_type"] = "mate_join_msg"
    
        elif isinstance(event, GroupDecreaseNoticeEvent): # 退群

            global_msg["msg_type"] = "mate_del_msg"

        ## print(f"\n\n\n{global_msg}\n\n\n")

        if event.group_id not in global_msg_notice_list:

            global_msg_notice_list[event.group_id] = []

        global_msg_notice_list[event.group_id].append(global_msg)

    except MatcherException as e:

        print(f"\n\n当前事件正常结束, 原文: {e}\n")

    except ProcessException as e:

        print(f"\n\n当前事件(通知接收)处理异常结束, 原文: {e}\n")

        await content_notice.finish(f"通知接收时发生了一些错误, 原文: {e}")