from django.db import models
from django.contrib.auth.models import User

class Field(models.Model):
    field = models.AutoField(primary_key=True)
    field_name = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.field_name

# Create your models here.
# class Specialization(models.Model):
#     specialization_id = models.AutoField(primary_key=True)
#     field = models.ForeignKey(Field, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     description = models.CharField(max_length=1000)
#     roadmap_id = models.IntegerField()

#     def __str__(self):
#         return self.title
    
#     class Meta:
#         unique_together = ('field')

        
class Specialization(models.Model):
    specialization_id = models.AutoField(primary_key=True)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    roadmap_id = models.IntegerField()

    def __str__(self):
        return self.title
    
    class Meta:
        unique_together = ('field',)  # Note the comma after 'field' to make it a tuple



# Optional if you want to add additional fields to the user model
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # Add additional fields as needed (e.g., profile picture, bio, etc.)

