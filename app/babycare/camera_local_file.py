import cv2
import time
import requests
import threading
from datetime import datetime


def send_video(file_path):
    url = "http://example.com/upload"
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(url, files=files)
        if response.status_code != 200:
            print("Failed to send video: {}".format(response.text))


def record_video(cap, out, start_time, duration, fourcc, framerate):
    ret, frame = cap.read()
    if ret:
        if time.time() - start_time >= duration:
            if out is not None:
                out.release()
                # threading.Thread(
                #     target=send_video, args=("{}.avi".format(current_time),)
                # ).start()
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            out = cv2.VideoWriter(
                "{}.avi".format(current_time), fourcc, framerate, (640, 480)
         s   )
            start_time = time.time()
        out.write(frame)
    return out, start_time


def main():
    framerate = 60.0
    duration = 10
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = None

    cap = cv2.VideoCapture("/dev/video0")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, framerate)

    start_time = time.time()
    while cap.isOpened():
        out, start_time = record_video(
            cap, out, start_time, duration, fourcc, framerate
        )
    cap.release()
    if out is not None:
        out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
