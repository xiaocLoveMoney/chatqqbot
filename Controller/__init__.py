import os.path

from Controller.ChatController import MyClient
import botpy
import yaml

from botpy import logging

from Service.DeepSeekService import DeepSeekService
from Service.MessageService import MessageService

_log = logging.get_logger()

class Controller():
    def __init__(self):
        _log.info("[Controller] 初始化机器人配置信息")
        ## 读取配置文件
        with open(os.path.join(os.getcwd(), "config", "config.yml"), 'r') as file:
            config: dict = yaml.safe_load(file)
            _log.info(f"[Controller] 机器人配置文件: {config}")

        # 订阅消息配置
        self.intents: dict = config["intents"]
        # 机器人登录配置
        self.loginToken: dict = config["botpy"]


        _log.info("初始化完成")

    def run(self):
        intents = botpy.Intents(**self.intents)
        client = MyClient(intents=intents)
        client.messageService = MessageService()
        client.run(**self.loginToken)