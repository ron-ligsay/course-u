from django.db import models
from django.contrib.auth.models import User

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
    
# class Test(models.Model):
#     question_id = models.AutoField(primary_key=True)
#     question = models.CharField(max_length=1000)
#     option1 = models.CharField(max_length=1000)
#     option2 = models.CharField(max_length=1000)
#     option3 = models.CharField(max_length=1000)
#     option4 = models.CharField(max_length=1000)
#     answer = models.CharField(max_length=1000)
#     topic = models.CharField(max_length=1000)

#     def __str__(self):
#         return self.question

class Test(models.Model):
    question_id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=1000)
    options = models.JSONField()  # Store options as a JSON field
    answer = models.CharField(max_length=1000)
    topic = models.CharField(max_length=1000)

    def __str__(self):
        return self.question

# class UserResponse(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming user authentication is used
#     question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
#     selected_option = models.ForeignKey(AnswerOption, on_delete=models.CASCADE)

# Optional if you want to add additional fields to the user model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add additional fields as needed (e.g., profile picture, bio, etc.)

# link,keyword,title,company,company_link,date
class JobPosting(models.Model):
    link_clean = models.CharField(max_length=5000)
    keyword = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    company_link = models.CharField(max_length=1000)
    #description = models.TextField()
    #requirements = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.title