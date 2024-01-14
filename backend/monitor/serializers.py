from rest_framework import serializers
from .models import ImageModel, NginxRTMPToken, BabyMonitorData


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ["id", "data", "timestamp"]


class VideoUploadSerializer(serializers.Serializer):
    """
    验证上传的监控视频
    """

    video = serializers.FileField(max_length=None, allow_empty_file=False)


class RTMPTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = NginxRTMPToken
        fields = "__all__"


class BabyMonitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BabyMonitorData
        fields = "__all__"
