"""
大模型相关的封装和调用
"""

import os
import requests
import json
import base64

from logger import logger


# 读取图片并编码为 Base64 字符串
def encode_image_to_base64(image_path=None, image_bytes=None):
    if image_path and image_bytes:
        raise ValueError("image_path and image_bytes cannot be both provided.")
    if image_path:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    if image_bytes:
        encoded_string = base64.b64encode(image_bytes).decode("utf-8")
    return encoded_string


def azure_gpt4o(message):
    api_key = os.getenv("API_KEY")
    headers = {"Content-Type": "application/json", "api-key": api_key}

    data = {
        "messages": message,
        "max_tokens": 4096,
        "temperature": 0.8,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "top_p": 0.95,
        "stop": None,
    }

    url = os.environ.get("GPT4O_ENDPOINT")
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            logger.info(
                f"LLM 调用失败，状态码：{response.status_code}，错误信息：{response.text}"
            )
    except requests.RequestException as e:
        logger.error(f"请求发生错误：{e}")
    except Exception as e:
        logger.error(f"发生未知错误：{e}")
