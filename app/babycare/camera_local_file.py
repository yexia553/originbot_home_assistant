import cv2
import time

# 获取摄像头
cap = cv2.VideoCapture(0)

# 设置帧率和分辨率
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 定义视频编码器
fourcc = cv2.VideoWriter_fourcc(*"XVID")

# 计数器和时间戳
counter = 0
start_time = time.time()

# 初始化视频写入对象
out = cv2.VideoWriter("output" + str(counter) + ".avi", fourcc, 30.0, (640, 480))

while True:
    # 读取帧
    ret, frame = cap.read()
    if not ret:
        break

    # 每10秒创建并保存新的视频文件
    if int(time.time() - start_time) >= 10:
        out.release()
        counter += 1
        out = cv2.VideoWriter(
            "output" + str(counter) + ".avi", fourcc, 30.0, (640, 480)
        )
        start_time = time.time()

    # 写入帧
    out.write(frame)

    # 显示帧
    cv2.imshow("frame", frame)

    # 按 'q' 键退出
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 释放摄像头和写入器
cap.release()
out.release()
cv2.destroyAllWindows()
