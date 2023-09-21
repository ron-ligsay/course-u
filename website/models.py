from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Specialization(models.Model):
    specialization_id = models.AutoField(primary_key=True)
    field_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    roadmap_id = models.IntegerField()


    def __str__(self):
        return self.title

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
    question = models.ForeignKey(Test, on_delete=models.CASCADE) 
    selected_option = models.IntegerField() # Index of the selected option in the options list
    is_correct = models.BooleanField()
    set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f"set: {self.set}, {self.question.question}"
    class Meta:
        unique_together = ('question','set') 

# Optional if you want to add additional fields to the user model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add additional fields as needed (e.g., profile picture, bio, etc.)

