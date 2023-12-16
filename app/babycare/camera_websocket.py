import asyncio
import cv2
import websockets
import time


async def send_frame(uri):
    cap = cv2.VideoCapture(0)  # 使用第一个摄像头
    if not cap.isOpened():
        print("Could not open video source")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)

    try:
        async with websockets.connect(uri) as websocket:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # 将图像编码为 JPEG 格式
                ret, jpeg = cv2.imencode(".jpg", frame)
                if not ret:
                    print("Could not encode frame to JPEG")
                    break
                await websocket.send(jpeg.tobytes())

    finally:
        cap.release()


asyncio.run(send_frame("ws://10.11.12.173:8000/ws/babycare/"))
