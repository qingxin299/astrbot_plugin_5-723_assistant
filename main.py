from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.core.utils.astrbot_path import get_astrbot_data_path


import re
from .randomFood import *

plugin_data_path = get_astrbot_data_path()
@register("5-723_assistant", "qing_xin", "一个简单的个人bot插件，致力于贝壳便捷生活", "0.0.1")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context) 

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
        self.foodData = {
            '外卖':{
            },
            '食堂':{
            }
        }
        #从文件读取有关的食物信息
        try:
            with open(plugin_data_path + '/randomFood.txt','r', encoding='utf-8') as f:
                for line in f.read().split('\n'):
                    tempList = list(line.split(','))
                    if len(tempList) < 3 or tempList[0] not in ['外卖','食堂']:
                        logger.error(f"randomFood.txt中的{line}不合法！")
                    self.foodData[tempList[0]][tempList[1]] = tempList[2]
        #如果文件不存在则创建一个空白文件
        except FileNotFoundError:
            with open(plugin_data_path + '/randomFood.txt','w', encoding='utf-8') as f:
                f.write('外卖,1+1随心配,麦当劳')



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
        message_str:str = event.message_str
        e = message_str.find('吃什么')
        if e != -1:
            yield event.plain_result(roll(event.message_str, self.foodData, message_str[e-2:e]))