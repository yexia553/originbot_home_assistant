import cv2
import datetime
import time


# 获取摄像头
cap = cv2.VideoCapture(0)

# 设置帧率和分辨率
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 获取当前时间
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))

# 循环获取视频帧并保存
while True:
    # 获取一帧视频
    ret, frame = cap.read()
    if not ret:
        break

    # 生成文件名
    filename = now.strftime("%Y-%m-%d_%H-%M-%S.mp4")

    # 保存视频帧
    out = cv2.VideoWriter(
        filename,
        cv2.VideoWriter_fourcc("M", "P", "4", "V"),
        30,
        (frame.shape[1], frame.shape[0]),
    )
    out.write(frame)
    out.release()

    # 休眠10秒
    time.sleep(10)

# 释放摄像头
cap.release()
