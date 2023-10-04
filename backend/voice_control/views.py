from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.asr.v20190614 import asr_client, models
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64
import json
import time
import logging

from utils.chatgpt import ChatGPT
from utils import envs


logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


class VoiceControl(APIView):
    def post(self, request, *args, **kwargs):
        audio_file = request.data.get('audio_file')

        if not audio_file:
            return Response({'status': 'error', 'message': '没有接收到音频数据'})

        assert isinstance(audio_file, InMemoryUploadedFile)

        audio_bytes = audio_file.read()
        if audio_bytes == b'':
            return Response({'status': 'error', 'message': '音频数据为空'})
        try:
            cred = credential.Credential(
                envs.TENCENT_SECRET_ID , envs.TENCENT_SECRET_KEY
            )
            httpProfile = HttpProfile()
            httpProfile.endpoint = "asr.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = asr_client.AsrClient(cred, "ap-shanghai", clientProfile)

            req = models.CreateRecTaskRequest()
            params = {
                "EngineModelType": "16k_zh",
                "ChannelNum": 1,
                "ResTextFormat": 3,
                "SourceType": 1,
                "Data": base64.b64encode(audio_bytes).decode('utf-8'),
            }
            req.from_json_string(json.dumps(params))
            resp = client.CreateRecTask(req)
            taskId = json.loads(resp.to_json_string())["Data"]["TaskId"]
            try:
                # 轮询获取任务结果
                while True:
                    time.sleep(1)
                    req = models.DescribeTaskStatusRequest()
                    params = {"TaskId": taskId}
                    req.from_json_string(json.dumps(params))
                    resp = client.DescribeTaskStatus(req)
                    status = json.loads(resp.to_json_string())["Data"]["Status"]

                    if status == 2:  # 任务完成
                        transcript = json.loads(resp.to_json_string())["Data"]["Result"]
                        logging.info('识别结果:', transcript)
                        chat = ChatGPT()
                        chat.generate(user_input=transcript)
                        return Response({'status': 'success', 'transcript': transcript})
                    elif status == 3:  # 任务失败
                        return Response({'status': 'error', 'message': '语音识别任务失败'})
            except Exception as e:
                return Response({'status': 'error', 'message': f'语音识别服务出错：{str(e)}'})
        except TencentCloudSDKException as err:
            return Response({'status': 'error', 'message': f'语音识别服务出错：{str(err)}'})

    def get(self, request, *args, **kwargs):
        return Response({'status': 'error', 'message': '无效的请求方法'})
