from django.db import models


class ImageModel(models.Model):
    data = models.TextField()  # Store base64 image string here.
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
