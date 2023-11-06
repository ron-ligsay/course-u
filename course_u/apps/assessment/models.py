from django.db import models
from django.contrib.auth.models import User
from django import forms

from apps.website.models import Field, Skill

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

     # Add the many-to-many relationship with Skill
    skills = models.ManyToManyField(Skill)

    def __str__(self):
        return self.question

    # class Meta:
        #allow field to have duplicate values
        # unique_together = ('field',)

class QuestionSet(models.Model):
    set_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    n_questions = models.IntegerField()
    is_completed = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    year = models.PositiveIntegerField(default=1)  # Add the year field

    def __str__(self):
        return f"{self.set_id}: Status : {self.is_completed} by User: {self.user} (Score: {self.score} / {self.n_questions}) "

    class Meta:
        unique_together = ('user', 'year')  # Enforce uniqueness based on user and year


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
