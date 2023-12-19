from utils.api_connection import APIConnection


conn = APIConnection()

vide_file = open(
    "/home/zhixiang_pan/learningspace/originbot_home_assistant/backend/big_buck_bunny.mp4",
    "rb",
)
file = {"video": vide_file}
res = conn.upload_video("api/monitor/video-upload/", file)
