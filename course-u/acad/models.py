from django.db import models
from django.contrib.auth.models import User

from website.models import Skill

class Course(models.Model):
    course_name = models.CharField(max_length=255)
    number_of_years = models.PositiveIntegerField()
    description = models.TextField()

    def __str__(self):
        return self.course_name

class Subject(models.Model):
    subject_name = models.CharField(max_length=255)
    description = models.TextField()
    
     # Add the many-to-many relationship with Skill
    skills = models.ManyToManyField(Skill)

    def __str__(self):
        return self.subject_name

class Curriculum(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()

    def __str__(self):
        return self.course.course_name + " - " + self.subject.subject_name + " - " + str(self.year)
    

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_student = models.BooleanField(default=False)
    enrolled_courses = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True)
    current_year = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    
class StudentGrades(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    
    def __str__(self):
        return self.student.user.username + " - " + self.subject.subject_name + " - " + str(self.grade)
    
    class Meta:
        unique_together = ('student', 'subject')
    
