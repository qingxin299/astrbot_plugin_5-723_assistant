from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.core.utils.astrbot_path import get_astrbot_data_path


import re
from .randomFood import *

plugin_data_path = get_astrbot_data_path() / "plugin_data" / self.name
@register("5-723_assistant", "qing_xin", "一个简单的个人bot插件，致力于贝壳便捷生活", "0.0.1")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
        logger.info(f"数据路径：{plugin_data_path}")
        #从文件读取有关的食物信息
        try:
            with open(plugin_data_path / 'randomFood.txt','r', encoding='utf-8') as f:
                self.foodData = f.read()
        #如果文件不存在则创建一个空白文件
        except FileNotFoundError:
            with open(plugin_data_path / 'randomFood.txt','w', encoding='utf-8') as f:
                self.foodData = f.write('test')



    @filter.command("ping")
    async def test_handler(self, event: AstrMessageEvent):
        """这是一个测试指令""" 
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        yield event.plain_result(f"pong!") # 发送一条纯文本消息

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""


    @filter.event_message_type(filter.EventMessageType.ALL)
    async def randomFood_handler(self, event: AstrMessageEvent):
        yield event.plain_result(roll(event.message_str, self.foodData))