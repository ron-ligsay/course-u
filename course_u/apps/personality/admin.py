from django.contrib import admin
from apps.personality.models import MBTI, MBTISet, MBTIResponse, Indicator

# Register your models here.
admin.site.register(MBTI)
admin.site.register(MBTISet)
admin.site.register(MBTIResponse)
admin.site.register(Indicator)