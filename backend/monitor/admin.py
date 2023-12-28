from django.contrib import admin
from .models import ImageModel, NginxRTMPToken, Baby, BabyMonitorData

admin.site.register(ImageModel)
admin.site.register(NginxRTMPToken)
admin.site.register(Baby)
admin.site.register(BabyMonitorData)
