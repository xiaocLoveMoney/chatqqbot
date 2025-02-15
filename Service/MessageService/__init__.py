import re

from botpy.message import C2CMessage

from Service.DeepSeekService import DeepSeekService


class MessageService:
    def __init__(self):
        self.deepSeekService: list = []

    # 检查聊天是否存在，并导出聊天
    def CheckOutDeepSeekService(self, user_openid, name) -> DeepSeekService:
        for _ in self.deepSeekService:
            if _.user_openid == user_openid:
                return _
        else:
            ds = DeepSeekService(user_openid, name)
            self.deepSeekService.append(ds)
            return ds

        # 删除聊天缓存
    def DeleteDeepSeekService(self, user_openid) -> DeepSeekService:
        print(self.deepSeekService, len(self.deepSeekService))
        for i in range(len(self.deepSeekService)):
            if self.deepSeekService[i].user_openid == user_openid:
                del self.deepSeekService[i]

    # 导出聊天记录
    def OutputMessages(self, ds: DeepSeekService) -> list:
        return ds.get_messages()

    # 检查是否存在命令
    def CheckCommend(self, message: str) -> bool:
        return re.match(r'^/', message)

    # 处理接受私聊消息
    def c2c_public_message(self, message: C2CMessage) -> str:
        user_openid: str = message.author.user_openid
        content: str = message.content

        ds = self.CheckOutDeepSeekService(user_openid=user_openid, name=message.content)

        # 检查是否是命令输出
        if self.CheckCommend(message.content):
            # 裁剪命令
            cmd: str = content.split(" ")[0]
            if cmd == "/重置会话":
                self.DeleteDeepSeekService(user_openid)
                return "重置成功"
            elif cmd == "/当前聊天记录":
                messages: list = ds.get_messages()
                result = [f"{_['role']}: {_['content']}\n" for _ in messages]
                res = ""
                for e in result:
                    res += e
                return res
            elif cmd == "/聊天记录":
                chats: list = ds.get_chats()
                result = [f"{_['chat_id']}: {_['name']}\n" for _ in chats]
                res = ""
                for e in result:
                    res += e
                return res

            elif re.match(r'^/\d+', cmd):
                chat_id = cmd.replace("/", "")
                messages: list = ds.get_messages_by_chat_id(chat_id)
                if not messages:
                    return "导入失败，暂无该记录"
                result = [f"{_['role']}: {_['content']}\n" for _ in messages]
                res = ""
                for e in result:
                    res += e
                return res
            return "操作失败，无对应命令"

        ds.set_message("user", content)

        return ds.send_message()
