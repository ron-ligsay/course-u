from django.contrib import admin
from .models import Specialization, Field, Skill, UserRecommendations
#, UserProfile


# Register your models here.
admin.site.register(Specialization)
#admin.site.register(UserProfile)
admin.site.register(Field)
admin.site.register(Skill)
admin.site.register(UserRecommendations)