from django.urls import include, path
from rest_framework import routers
from monitor.views import ImageViewSet, stream_video, VideoUploadView, RTMPAuthView

router = routers.DefaultRouter()
router.register("images", ImageViewSet, basename="images")
router.register("video", VideoUploadView, basename="video")
router.register("rtmp-token", RTMPAuthView, basename="rtmp-token")

urlpatterns = [
    path("", include(router.urls)),
    path("video-stream/", stream_video, name="stream-video"),
] + router.urls
