import os
import re

import yaml
from botpy import logging
from openai import OpenAI

from Mapper import Mapper

_log = logging.get_logger()


class DeepSeekService:
    def __init__(self, user_openid, name):
        # 初始化数据库持久类
        self.mysql = Mapper()

        _log.info("[DeepSeekService] DeepSeek 配置信息")
        ## 读取配置文件
        with open(os.path.join(os.getcwd(), "config", "deepseek.yml"), 'r') as file:
            config: dict = yaml.safe_load(file)
            _log.info(f"[DeepSeekService] DeepSeek配置文件: {config}")

        # 获取基础配置
        base_info = config["deepseek"]

        # 初始化信息
        self.client = OpenAI(**base_info)

        # 初始化聊天临时记录
        self.user_openid: int = user_openid
        self.role = []
        self.content = []

        # 新增消息
        self.chat_id = self.mysql.execute_insert_query("insert into chat(user_openid, name) values (%s, %s)", (user_openid, name))
        _log.info(f"[DeepSeekService] 新增消息缓存 编号：{self.chat_id}")


        _log.info("[DeepSeekService] DeepSeek 初始化完成")

    # 导出缓存聊天记录
    def get_messages(self) -> list:
        return [{"role": _[0], "content": _[1]} for _ in zip(self.role, self.content)]

    # 导入缓存聊天记录
    def set_messages(self, messages: list) -> None:
        role = []
        content = []
        for message in messages:
            role.append(message["role"])
            content.append(message["content"])
        self.role = role
        self.content = content

    # 导入单条消息
    def set_message(self,role: str, message: str) -> None:
        _log.info(f"[DeepSeekService] {role} -> {message}")
        self.mysql.execute_insert_query("insert into message(chat_id, role, content) values(%s, %s, %s)", (self.chat_id, role, message))
        self.role.append(role)
        self.content.append(message)

    # 获取回答
    def send_message(self) -> str:
        completion = self.client.chat.completions.create(
            model="qwen-plus",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            messages=self.get_messages()
        )
        result_message = completion.choices[0].message
        self.set_message(result_message.role, result_message.content)
        return result_message.content

    # 获取历史聊天
    def get_chats(self):
        return self.mysql.execute_sql_query("select * from chat where user_openid = %s" , (self.user_openid))

    # 聊天编号获取聊天记录并导入
    def get_messages_by_chat_id(self, chat_id):
        self.chat_id = chat_id
        messages_list: list = self.mysql.execute_sql_query("select * from message where chat_id = %s" , (self.chat_id))
        if len(messages_list) == 0:
            return False
        self.set_messages(messages_list)
        return messages_list

    def __del__(self):
        return "操作成功"