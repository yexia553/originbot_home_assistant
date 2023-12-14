from django.urls import re_path
from monitor import ws_consumers


websocket_urlpatterns = [
    re_path("babycare/", ws_consumers.BabyCare.as_asgi()),
]
