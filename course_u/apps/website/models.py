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
    explanation = models.CharField(max_length=1000, default='')

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

class SpecializationSkills(models.Model):
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.specialization.title} - {self.skill.skill}"

    class Meta:
        unique_together = ('specialization', 'skill')

class LearningMaterial(models.Model):
    material_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300)
    university = models.CharField(max_length=100)
    level = models.CharField(max_length=100)
    rating = models.FloatField(default=0)
    url = models.CharField(max_length=1000)
    description = models.CharField(max_length=3000)
    skills = models.CharField(max_length=1000)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
