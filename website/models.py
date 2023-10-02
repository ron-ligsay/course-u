from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Specialization(models.Model):
    specialization_id = models.AutoField(primary_key=True)
    field_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    roadmap_id = models.IntegerField()


    def __str__(self):
        return self.title



# Optional if you want to add additional fields to the user model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add additional fields as needed (e.g., profile picture, bio, etc.)

