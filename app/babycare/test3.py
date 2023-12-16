import asyncio
import cv2
import websockets
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=2)


async def send_frame(uri):
    cap = cv2.VideoCapture(0)  # 使用第一个摄像头
    if not cap.isOpened():
        print("Could not open video source")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)

    # Initialize an empty frame and encoding future
    frame, encoding_future = None, None

    try:
        async with websockets.connect(uri) as websocket:
            while True:
                # If there's a frame waiting, get its encoding future
                if frame is not None:
                    # Wait for the frame to be encoded
                    jpeg = await encoding_future

                    if jpeg is None:
                        print("Could not encode frame to JPEG")
                        break

                    await websocket.send(jpeg.tobytes())

                # Read the next frame
                ret, frame = cap.read()

                if not ret:
                    break

                # Start encoding the frame in a separate thread
                encoding_future = loop.run_in_executor(executor, encode_frame, frame)

    finally:
        cap.release()


def encode_frame(frame):
    # Encode the frame into JPEG format
    ret, jpeg = cv2.imencode(".jpg", frame)
    return jpeg if ret else None


loop = asyncio.get_event_loop()
loop.run_until_complete(send_frame("ws://10.11.12.173:8000/ws/babycare/"))
