from django.db import models


class ImageModel(models.Model):
    data = models.TextField()  # Store base64 image string here.
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]


class NginxRTMPToken(models.Model):
    password = models.CharField(max_length=128)
    username = models.CharField(max_length=128)
