import cv2
import datetime
import time


# 获取摄像头
cap = cv2.VideoCapture(0)

# 设置帧率和分辨率
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


try:
    while True:
        # 获取当前时间
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
        # 生成文件名
        filename = now.strftime("%Y-%m-%d_%H-%M-%S.avi")
        # 保存视频帧
        out = cv2.VideoWriter(
            filename,
            cv2.VideoWriter_fourcc(*"XVID"),
            30,
            (640, 480),
        )
        # 循环获取视频帧并保存
        start_time = time.time()
        while True:
            # 获取一帧视频
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
            if int(time.time() - start_time) > 10:
                out.release()
                continue

finally:
    # 释放摄像头
    cap.release()
