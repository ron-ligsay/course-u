from django.db import models
from django.contrib.auth.models import User

class Skill(models.Model):
    skill = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.skill

class Field(models.Model):
    field = models.AutoField(primary_key=True)
    field_name = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.field_name

class Specialization(models.Model):
    specialization_id = models.AutoField(primary_key=True)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    roadmap_id = models.IntegerField()
    

    def __str__(self):
        return self.title
    # allow field id to have duplicates
    # class Meta:
    #     unique_together = ('field')

class UserRecommendations(models.Model):
    recommendation_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    field_1 = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='field_1', null=True, blank=True)
    field_2 = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='field_2', null=True, blank=True)
    field_3 = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='field_3', null=True, blank=True)
    score_1 = models.FloatField(null=True, blank=True)
    score_2 = models.FloatField(null=True, blank=True)
    score_3 = models.FloatField(null=True, blank=True)
    # You can add other fields here for additional information, such as scores, timestamps, etc.

    def __str__(self):
        return f"Recommendations for User: {self.user.username}"

    class Meta:
        ordering = ['user']  # Specify the default ordering for UserRecommendations

