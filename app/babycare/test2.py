import cv2
import time
import sounddevice as sd
import numpy as np
import threading

# 录制视频
def record_video():
    cap = cv2.VideoCapture('/dev/video0')  # 使用你提供的设备路径
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
    start_time = time.time()
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            out.write(frame)
            if time.time() - start_time > 30:
                break
        else:
            break
    cap.release()
    out.release()

# 录制音频
def record_audio():
    fs = 44100  # 采样率
    duration = 30  # 录音时长
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()  # 等待录音结束
    sd.write('output.wav', myrecording, fs)

# 开始录制
video_thread = threading.Thread(target=record_video)
audio_thread = threading.Thread(target=record_audio)

video_thread.start()
audio_thread.start()

video_thread.join()
audio_thread.join()
