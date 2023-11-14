from django.contrib import admin
from apps.acad.models import Course, Subject, Curriculum, StudentGrades, StudentProfile

# Register your models here.
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Curriculum)
admin.site.register(StudentGrades)
admin.site.register(StudentProfile)