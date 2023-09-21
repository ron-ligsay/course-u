from django.db import models
from django.contrib.auth.models import User
from django import forms

# Create your models here.
class Test(models.Model):
    question_id = models.AutoField(primary_key=True)
    topic = models.CharField(max_length=1000)
    question = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    options = models.JSONField()
    correct_option = models.IntegerField() # Index of the correct option in the options list

    def __str__(self):
        return self.question

class QuestionSet(models.Model):
    set_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    n_questions = models.IntegerField()
    is_completed = models.BooleanField(default=False)
    score = models.IntegerField(default=0)

    def __str__(self):
        return str(self.set_id)
    class Meta:
        unique_together = ('user',)

class UserResponse(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.AutoField(primary_key=True,serialize=False, auto_created=True)
    question = models.ForeignKey(Test, on_delete=models.CASCADE) 
    selected_option = models.IntegerField() # Index of the selected option in the options list
    is_correct = models.BooleanField()
    is_answered = models.BooleanField(default=False)
    set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f"set: {self.set}, {self.question_id}"
    class Meta:
        unique_together = ('question','set') 