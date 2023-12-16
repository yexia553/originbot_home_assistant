import ffmpeg
import requests

input_device = "/dev/video0"
server_url = "http://10.11.12.173:8000/api/monitor/hlsendpoint/"  # 你的服务器地址

try:
    process1 = (
        ffmpeg.input(input_device)
        .output(
            "pipe:",
            format="hls",
            hls_time=4,
            hls_list_size=1,
            hls_wrap=4,
            hls_flags="delete_segments",
        )
        .run_async(pipe_stdout=True, pipe_stderr=True)
    )

    segment = b""
    while True:
        output = process1.stdout.read(1024)
        if not output:
            break
        segment += output
        if b"#EXT-X-ENDLIST" in segment:  # 当 HLS segment 完成时
            response = requests.post(server_url, data=segment)  # 发送到服务器
            if response.status_code == 200:
                print("Segment sent successfully")
            else:
                print("Failed to send segment")
            segment = b""  # 重置 segment
except ffmpeg.Error as e:
    print("ffmpeg Error:", e.stderr.decode())
