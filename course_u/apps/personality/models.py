from django.db import models
from django.contrib.auth.models import User
from django import forms

from apps.website.models import Field, Skill

# Create your models here.
class MBTI(models.Model):
    mbti = models.AutoField(primary_key=True,serialize=False, auto_created=True)
    mbti_question = models.CharField(max_length=1000)
    option_a = models.CharField(max_length=1000)
    option_b = models.CharField(max_length=1000)
    ans_a = models.CharField(max_length=15)
    ans_b = models.CharField(max_length=15)
    acr_a = models.CharField(max_length=1, default='a')
    acr_b = models.CharField(max_length=1, default='b')

    def __str__(self):
        return f"{self.mbti_question} ({self.ans_a}/{self.ans_b})"
    


class Indicator(models.Model):
    indicator_id = models.AutoField(primary_key=True,serialize=False, auto_created=True)
    indicator = models.CharField(max_length=4)
    indicator_name = models.CharField(max_length=50)
    indicator_description = models.CharField(max_length=1000)

    skills = models.ManyToManyField(Skill)

    def __str__(self):
        return f"{self.indicator} ({self.indicator_type})"


class MBTISet(models.Model):
    mbti_set_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    # float values 1 - 5
    mind = models.FloatField(default=0)
    energy = models.FloatField(default=0)
    nature = models.FloatField(default=0)
    tactics = models.FloatField(default=0)
    
    indicator =  models.ForeignKey(Indicator, on_delete=models.CASCADE, null=True, blank=True)
    # let identity to be null
    identity = models.CharField(max_length=4, null=True, blank=True)

    def __str__(self):
        return f"{self.mbti_set_id}: Status : {self.is_completed} by User: {self.user} (Identity: {self.identity}) "
    
    class Meta:
        unique_together = ('user',)

# class Option:
#     def __init__(self):
#         self._selected_option = 0

#     @property
#     def selected_option(self):
#         return self._selected_option

#     @selected_option.setter
#     def selected_option(self, value):
#         if -3 <= value <= 3:
#             self._selected_option = value
#         else:
#             raise ValueError("Option must be between -3 and 3")


class MBTIResponse(models.Model):
    mbti_response_id = models.AutoField(primary_key=True,serialize=False, auto_created=True)
    mbti_set = models.ForeignKey(MBTISet, on_delete=models.CASCADE, null=True, blank=True)
    mbti = models.ForeignKey(MBTI, on_delete=models.CASCADE)
    is_answered = models.BooleanField(default=False)
    #  make selected_option ranges from -3 to 3, default = 0 
    selected_option = models.IntegerField(default=0)

    def __str__(self):
        return f"Set: {self.mbti_set.mbti_set_id}, Question: {self.mbti_response_id}"
    
    class Meta:
        unique_together = ('mbti_set','mbti')


