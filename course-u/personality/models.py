from django.db import models
from django.contrib.auth.models import User
from django import forms



# Create your models here.
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
    selected_option = models.IntegerField(null=True, blank=True) 

    def __str__(self):
        return f"Set: {self.mbti_set.mbti_set_id}, Question: {self.mbti_response_id}"
    
    class Meta:
        unique_together = ('mbti_set','mbti')