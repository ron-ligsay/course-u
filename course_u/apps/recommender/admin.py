from django.contrib import admin
from .models import UserSkill, UserSkillSource, UserRecommendations
# Register your models here.

admin.site.register(UserSkill)
admin.site.register(UserSkillSource)
admin.site.register(UserRecommendations)