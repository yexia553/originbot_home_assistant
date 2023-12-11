import cv2
import subprocess as sp

# 视频源，你可以改为你自己的视频文件，或者是网络流媒体地址，或者是摄像头设备
cap = cv2.VideoCapture('/dev/video0')

# 获取视频的宽度和高度
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# ffmpeg 命令
command = [
    'ffmpeg',
    '-y',  # 覆盖输出文件
    '-f', 'rawvideo',
    '-vcodec', 'rawvideo',
    '-s', '{}x{}'.format(frame_width, frame_height),  # size of one frame
    '-pix_fmt', 'bgr24',  # opencv uses bgr format
    '-r', '25',  # frames per second
    '-i', '-',  # The input comes from a pipe
    '-an',  # Tells FFMPEG not to expect any audio
    '-vcodec', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-preset', 'ultrafast',
    '-f', 'flv',
    'rtmp://10.11.12.173:1935/live/test'  # RTMP server
]

# 开启一个子进程
ffmpeg = sp.Popen(command, stdin=sp.PIPE)

while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break

    # 将 opencv 的图片通过 pipe 发送到 ffmpeg
    ffmpeg.stdin.write(frame.tobytes())

# 释放所有资源
cap.release()
ffmpeg.stdin.close()
ffmpeg.wait()
