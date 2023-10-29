from django.urls import include, path
from rest_framework import routers
from monitor.views import ImageViewSet, stream_video

router = routers.DefaultRouter()
router.register(r'images', ImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('video-stream/', stream_video, name='stream-video'),
]
