from django.db import models
from django.contrib.auth.models import User
from django import forms

from website.models import Field

TEST_TOPICS = (
    ('Python', 'Python'),
)

# Create your models here.
class Test(models.Model):
    question_id = models.AutoField(primary_key=True, serialize=False, auto_created=True)
    field = models.ForeignKey(Field, on_delete=models.CASCADE, null=True, blank=True)
    question = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    options = models.JSONField()
    correct_option = models.IntegerField() # Index of the correct option in the options list

    def __str__(self):
        return self.question

    class Meta:
        unique_together = ('field',)

class QuestionSet(models.Model):
    set_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    n_questions = models.IntegerField()
    is_completed = models.BooleanField(default=False)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.set_id}: Status : {self.is_completed} by User: {self.user} (Score: {self.score} / {self.n_questions}) "#str(self.set_id)
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
        return f"Set: {self.set.set_id}, Question: {self.question_id}"
    class Meta:
        unique_together = ('question','set') 

class MBTI(models.Model):
    mbti = models.AutoField(primary_key=True,serialize=False, auto_created=True)
    mbti_question = models.CharField(max_length=1000)
    option_a = models.CharField(max_length=1000)
    option_b = models.CharField(max_length=1000)
    ans_a = models.CharField(max_length=15)
    ans_b = models.CharField(max_length=15)
    acr_a = models.CharField(max_length=1)

    def __str__(self):
        return f"{self.mbti_question} ({self.ans_a}/{self.ans_b})"
    
class MBTISet(models.Model):
    mbti_set_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    # float values 1 - 5
    mind = models.FloatField(default=0)
    energy = models.FloatField(default=0)
    nature = models.FloatField(default=0)
    tactics = models.FloatField(default=0)
    # identity is the personality type
    identity = models.CharField(max_length=5, default="")

    def __str__(self):
        return f"{self.mbti_set_id}: Status : {self.is_completed} by User: {self.user} (Identity: {self.identity}) "
    
    class Meta:
        unique_together = ('user',)

class MBTIResponse(models.Model):
    mbti_response_id = models.AutoField(primary_key=True,serialize=False, auto_created=True)
    mbti_set = models.ForeignKey(MBTISet, on_delete=models.CASCADE, null=True, blank=True)
    mbti = models.ForeignKey(MBTI, on_delete=models.CASCADE)
    is_answered = models.BooleanField(default=False)
    selected_option = models.IntegerField()

    def __str__(self):
        return f"Set: {self.mbti_set.mbti_set_id}, Question: {self.mbti_response_id}"
    
    class Meta:
        unique_together = ('mbti_set','mbti')