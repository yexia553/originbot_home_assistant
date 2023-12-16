"""
在客户端使用
ffmpeg -i /dev/video0 -f hls -hls_time 4 -hls_list_size 1 -hls_wrap 4 -hls_flags delete_segments stream.m3u8
获取hls格式的文件，然后用这个脚本发送出去
"""
import requests
import os
import time

# the directory where the HLS segments and m3u8 file are saved
directory = "/root/workspace/originbot_home_assistant/app/babycare/"
# the URL of your Django server
url = "http://10.11.12.173:8000/api/monitor/hlsendpoint/"

while True:
    for filename in os.listdir(directory):
        if filename.endswith(".ts") or filename.endswith(".m3u8"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "rb") as f:
                files = {"file": (filename, f)}
                response = requests.put(url, files=files)
                # handle the response, e.g., check if it's successful
            # delete the file after it's sent
            os.remove(filepath)
    # sleep for a while before the next round
    time.sleep(0.5)
