"""
在本地生成视频文件
"""
import cv2
import time
from datetime import datetime

# 定义帧率和持续时间
framerate = 30.0
duration = 10

# 定义编解码器并创建 VideoWriter 对象
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = None

cap = cv2.VideoCapture("/dev/video0")

# 设置分辨率
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, framerate)

start_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if ret == True:
        # 判断是否需要创建新的 VideoWriter 对象（即是否已经过了 10 秒）
        if time.time() - start_time >= duration:
            if out is not None:
                out.release()
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            out = cv2.VideoWriter(
                "{}.avi".format(current_time), fourcc, framerate, (640, 480)
            )
            start_time = time.time()
        # 写入帧
        out.write(frame)
    else:
        break

# 释放资源
cap.release()
if out is not None:
    out.release()

cv2.destroyAllWindows()
