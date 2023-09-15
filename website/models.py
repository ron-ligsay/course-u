from django.db import models

# Create your models here.
class Specialization(models.Model):
    specialization_id = models.AutoField(primary_key=True)
    #field_id = models.IntegerField()
    field_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    roadmap_id = models.IntegerField()


    def __str__(self):
        return self.title
    
class Test(models.Model):
    question_id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=1000)
    option1 = models.CharField(max_length=1000)
    option2 = models.CharField(max_length=1000)
    option3 = models.CharField(max_length=1000)
    option4 = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000)
    topic = models.CharField(max_length=1000)

    def __str__(self):
        return self.question