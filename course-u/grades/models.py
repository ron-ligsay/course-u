from django.contrib.auth.models import User
from django.db import models

# Define the course and year choices
COURSE_CHOICES = [
    ('CS', 'Computer Science'),
    ('IT', 'Information Technology'),
]

YEAR_CHOICES = [
    ('1', '1st Year'),
    ('2', '2nd Year'),
    ('3', '3rd Year'),
    ('4', '4th Year'),
]

SUBJECT_CHOICES = [
    ('A', 'CYBERSECURITY'),
    ('B', 'DATA SCIENCE'),
    ('C', 'MULTIMEDIA'),
    ('D', 'MACHINE LEARNING'),
]

# Define possible grades
GRADE_CHOICES = [
    ('1', '1.0'),
    ('1.25', '1.25'),
    ('1.5', '1.5'),
    ('1.75', '1.75'),
    ('2', '2.0'),
    ('2.25', '2.25'),
    # ... Add all other grade choices up to 5.0
    ('5', '5.0'),
]

class Grade(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    subjectname = models.CharField(max_length=150, choices=SUBJECT_CHOICES)
    grade = models.CharField(max_length=4, choices=GRADE_CHOICES)
    course = models.CharField(max_length=150, choices=COURSE_CHOICES)
    year = models.CharField(max_length=150, choices=YEAR_CHOICES)
    