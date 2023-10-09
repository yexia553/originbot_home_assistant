from django.db import models


class Videos(models.Model):
    """
    监控视频或图片的模型类
    """
    name = models.CharField(max_length=256)
    video = models.FileField(upload_to='monitor_videos/%Y/%m/%d/')
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return self.name
