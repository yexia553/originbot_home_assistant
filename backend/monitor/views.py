from django.core.files.storage import FileSystemStorage
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import os
import glob
from datetime import date
from rest_framework import viewsets
from django.http import FileResponse
from django.conf import settings
from .models import ImageModel
from .serializers import ImageSerializer, VideoUploadSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all().order_by("-timestamp")
    serializer_class = ImageSerializer


def stream_video(request):
    video_file_path = str(settings.BASE_DIR) + "/output.mp4"

    response = FileResponse(open(video_file_path, "rb"))
    return response


class VideoUploadView(viewsets.ViewSet):
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        serializer = VideoUploadSerializer(data=request.data)
        if serializer.is_valid():
            file_obj = serializer.validated_data["video"]
            fs = FileSystemStorage(location=f"{settings.BASE_DIR}/media/monitor/")

            # 根据日期划分子目录
            today_folder = str(date.today())
            if not os.path.exists(os.path.join(fs.location, today_folder)):
                os.mkdir(os.path.join(fs.location, today_folder))

            # 检查具有AVI格式文件的数量，如果超过100个，则删除创建时间最早的文件
            avi_files = list(
                glob.glob(
                    os.path.join(os.path.join(fs.location, today_folder), "*.avi")
                )
            )
            if len(avi_files) > 360:  # 结合客户端是视频时长，360个视频文件是最近1小时的录像
                oldest_file = min(avi_files, key=os.path.getctime)
                os.remove(oldest_file)

            # 保存文件到指定路径
            video_path = fs.save(f"monitor/{today_folder}/{file_obj.name}", file_obj)

            return Response(
                {"message": f"Video {video_path} uploaded successfully."},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
