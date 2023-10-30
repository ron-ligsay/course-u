from django.contrib.auth.models import User
from django.db import models
    
class Subject(models.Model):
    subject_id = models.IntegerField(primary_key=True)
    course = models.CharField(max_length=1000)
    year = models.IntegerField()
    subject = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.subject_id} - {self.course} - {self.year} - {self.subject}"

class Student(models.Model):
    student_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.FloatField()

    def __str__(self):
        return f"{self.student_id} - {self.user} - {self.subject} - {self.grade}"
