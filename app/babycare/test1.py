import cv2
import time

cap = cv2.VideoCapture('/dev/video0')  # 使用你提供的设备路径

# 定义编解码器并创建VideoWriter对象
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

# 记录起始时间
start_time = time.time()

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        # 将帧写入文件
        out.write(frame)

        # 如果录制了10秒钟，就跳出循环
        if time.time() - start_time > 10:
            break
    else:
        break

# 完成后释放所有内容
cap.release()
out.release()
cv2.destroyAllWindows()
