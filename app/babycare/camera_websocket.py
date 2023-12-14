import asyncio
import cv2
import websockets
import time


async def send_frame(uri):
    cap = cv2.VideoCapture(0)  # 使用第一个摄像头
    if not cap.isOpened():
        print("Could not open video source")
        return

    try:
        async with websockets.connect(uri) as websocket:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            prev_frame_time = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # 将图像编码为 JPEG 格式
                ret, jpeg = cv2.imencode(".jpg", frame)
                if not ret:
                    print("Could not encode frame to JPEG")
                    break

                # 帧率控制，每秒30帧
                new_frame_time = time.time()
                if new_frame_time - prev_frame_time > 1.0 / 30:
                    # 发送 JPEG 二进制数据
                    await websocket.send(jpeg.tobytes())
                    prev_frame_time = new_frame_time
    finally:
        cap.release()


asyncio.run(send_frame("ws://10.11.12.173:8000/ws/babycare/"))
