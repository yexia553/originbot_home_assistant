import asyncio
import cv2
import websockets


async def send_frame(uri):
    cap = cv2.VideoCapture(0)  # 使用第一个摄像头

    async with websockets.connect(uri) as websocket:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # 将图像编码为 JPEG 格式
            ret, jpeg = cv2.imencode(".jpg", frame)
            if not ret:
                break

            # 发送 JPEG 二进制数据
            await websocket.send(jpeg.tobytes())

    cap.release()


asyncio.run(send_frame("ws://127.0.0.1:8000/ws/babycare/"))
