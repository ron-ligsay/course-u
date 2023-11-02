from django.contrib import admin
from personality.models import MBTI, MBTISet, MBTIResponse

# Register your models here.
admin.site.register(MBTI)
admin.site.register(MBTISet)
admin.site.register(MBTIResponse)