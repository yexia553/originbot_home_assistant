from rest_framework import serializers
from .models import Videos


class VideosSerializers(serializers.ModelSerializer):
    class Meta:
        model = Videos
        fields = '__all__'
