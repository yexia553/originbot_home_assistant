from rest_framework import routers
from django.urls import path
from voice_control import views


ROUTER = routers.DefaultRouter()

urlpatterns = [
    path('', views.VoiceControl.as_view(), name='voice_control'),
] + ROUTER.urls
