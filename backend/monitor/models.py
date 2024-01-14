from django.db import models
import uuid


class ImageModel(models.Model):
    data = models.TextField()  # Store base64 image string here.
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]


class NginxRTMPToken(models.Model):
    """存储Nginx RTMP 模块的认证数据"""

    password = models.CharField(max_length=128)
    username = models.CharField(max_length=128)


class Baby(models.Model):
    """
    记录的宝宝的数据
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    name = models.CharField(max_length=256)
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=(("男", "男"), ("女", "女")))

    def __str__(self):
        return self.name


class BabyMonitorData(models.Model):
    """
    记录宝宝监控相关的数据
    """

    event_choices = (
        ("看不到脸", "看不到脸"),
        ("哭", "哭"),
        ("翻身", "翻身"),
        ("不在摄像头范围内", "不在摄像头范围内"),
    )

    baby = models.ForeignKey(Baby, on_delete=models.PROTECT)
    event = models.CharField(max_length=128, choices=event_choices)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.baby.name} {self.event} {self.timestamp}"

    class Meta:
        ordering = ["-timestamp"]
