"""
用于钉钉单聊机器人收发消息
"""

from dingtalk_stream import AckMessage
import dingtalk_stream
import os

from prompts import base_prompt
from llms import azure_gpt4o


class DingtalkMsgHandler(dingtalk_stream.ChatbotHandler):
    prompt = base_prompt

    def __init__(self):
        super(dingtalk_stream.ChatbotHandler, self).__init__()

    def format_prompt(self, msg):
        """
        整个运行期间的对话都会被添加到prompt中
        TODO: 优化prompt动态管理方法
        """
        DingtalkMsgHandler.prompt.append(
            {
                "role": "user",
                "content": msg,
            }
        )
        return DingtalkMsgHandler.prompt

    async def process(self, callback: dingtalk_stream.CallbackMessage):
        incoming_message = dingtalk_stream.ChatbotMessage.from_dict(callback.data)
        message_type = incoming_message.message_type

        if message_type not in ("text"):
            self.reply_text(
                "您发送的消息类型不合法，目前只支持文本。", incoming_message
            )
            return AckMessage.STATUS_OK, "OK"

        if message_type == "text":
            text = incoming_message.text.content.strip()
            self.format_prompt(text)
            res = azure_gpt4o(DingtalkMsgHandler.prompt)
            self.reply_text(str(res), incoming_message)
            self.format_prompt(res)
            return AckMessage.STATUS_OK, "OK"


def main():
    credential = dingtalk_stream.Credential(
        os.getenv("DINGTALK_CLIENTID"),
        os.getenv("DINGTALK_CLIENTSECRET"),
    )
    client = dingtalk_stream.DingTalkStreamClient(credential)
    client.register_callback_handler(
        dingtalk_stream.chatbot.ChatbotMessage.TOPIC, DingtalkMsgHandler()
    )
    client.start_forever()


if __name__ == "__main__":
    main()
