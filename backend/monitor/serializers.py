from rest_framework import serializers
from .models import ImageModel


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ["id", "data", "timestamp"]


class VideoUploadSerializer(serializers.Serializer):
    """
    验证上传的监控视频
    """

    video = serializers.FileField(max_length=None, allow_empty_file=False)
