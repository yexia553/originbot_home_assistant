import cv2
import datetime
import time

# 获取摄像头
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise Exception("无法打开摄像头")

# 设置帧率和分辨率
cap.set(cv2.CAP_PROP_FPS, 5)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


def get_vidoe_out():
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    filename = now.strftime("%Y-%m-%d_%H-%M-%S.avi")
    out = cv2.VideoWriter(
        filename,
        cv2.VideoWriter_fourcc(*"XVID"),
        5,
        (1280, 720),
    )
    return out


try:
    split_interval_s = 10.0  # 设定每个录像文件的时长为10秒

    out = get_vidoe_out()
    start_time = time.time()
    while True:
        ret, frame = cap.read()

        if not ret:
            raise Exception("无法读取视频帧数据")

        elapsed_time = time.time() - start_time  # 计算已经过去的录像时间

        if elapsed_time > split_interval_s:  # 如超过设定的interval，则创建新的录像文件
            if out is not None:
                out.release()
            else:
                raise Exception("OpenCV VideoWriter对象为空，无法保存视频数据")

            out = get_vidoe_out()

            start_time = time.time()  # 更新start_time

        out.write(frame)

finally:
    cap.release()
    if out is not None:
        out.release()
