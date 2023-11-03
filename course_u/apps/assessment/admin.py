from django.contrib import admin
from .models import Test, QuestionSet, UserResponse

# Register your models here.
admin.site.register(Test)
admin.site.register(QuestionSet)
admin.site.register(UserResponse)