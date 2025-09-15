from pathlib import Path

import nonebot as nb

from nonebot.adapters.onebot import V11Adapter as OneBotAdapter  # 避免重复命名

"""准备工作"""
nb.init() # 初始化

driver = nb.get_driver() # 获取driver号

driver.register_adapter(OneBotAdapter) # 注册适配器

# nb.load_builtin_plugins("echo")  # 加载内置插件

nb.load_plugins(str(Path("local_plugins\\plugins").resolve()))  # 加载本地插件组

# nb.load_plugin("nonebot_plugin_cooldown")  # 加载本地单插件

if __name__ == "__main__":

    nb.run()