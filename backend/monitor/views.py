from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from django.shortcuts import render
from .serializers import VideosSerializers
from monitor.models import Videos
from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.files.base import File
import os
import logging


class VideosViewSet(ModelViewSet):
    queryset = Videos.objects.all()
    serializer_class = VideosSerializers
    ordering_fields = '-created_time'


class FileUploadView(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response(
                {'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST
            )

        video = Videos()
        video.name = file.name
        video.video.save(file.name, file)
        video.save()

        return Response(
            {'message': f'File {file.name} uploaded successfully.'},
            status=status.HTTP_200_OK,
        )


def home(request):
    videos = Videos.objects.all()
    paginator = Paginator(videos, 6)
    page_number = request.GET.get('page')
    paged_photos = paginator.get_page(page_number)
    context = {'photos': paged_photos}

    return render(request, 'watch_videos/endless_list.html', context)