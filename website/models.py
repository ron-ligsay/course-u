from django.db import models

# Create your models here.
class specialization(models.Model):
    specialization_id = models.AutoField(primary_key=True)
    #field_id = models.IntegerField()
    field_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    roadmap_id = models.IntegerField()


    def __str__(self):
        return self.specialization_name