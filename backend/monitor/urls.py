from django.urls import include, path
from rest_framework import routers
from monitor.views import (
    ImageViewSet,
    stream_video,
    VideoUploadView,
    RTMPAuthTokenView,
    RTMPAuthView,
    DingTalkView,
    BabyMonitorView,
)

router = routers.DefaultRouter()
router.register("images", ImageViewSet, basename="images")
router.register("video", VideoUploadView, basename="video")
router.register("rtmp-token", RTMPAuthTokenView, basename="rtmp-token")
router.register("face-detection", BabyMonitorView, basename="face-detection")

urlpatterns = [
    path("", include(router.urls)),
    path("video-stream/", stream_video, name="stream-video"),
    path("dingtalk/", DingTalkView.as_view(), name="dingtalk"),
    path("rtmp-auth/", RTMPAuthView.as_view(), name="rtmp-auth"),
] + router.urls
