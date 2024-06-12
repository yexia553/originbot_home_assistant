"""
通过webhook发送消息到钉钉群
"""

import json
import requests
from utils import envs


def send_msg_to_dingtalk(msg):
    webhook = envs.DING_TALK_URL
    headers = {"Content-Type": "application/json;charset=utf-8"}
    data = {"msgtype": "text", "text": {"content": msg}}

    response = requests.post(webhook, headers=headers, data=json.dumps(data))
    return response.text


if __name__ == "__main__":
    message = "Hello from my Python script!"
    send_msg_to_dingtalk(message)
