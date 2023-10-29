from rest_framework import viewsets
from django.http import FileResponse
from django.conf import settings
from .models import ImageModel
from .serializers import ImageSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all().order_by('-timestamp')
    serializer_class = ImageSerializer


def stream_video(request):
    video_file_path = str(settings.BASE_DIR) + '/output.mp4'

    response = FileResponse(open(video_file_path, 'rb'))
    return response
