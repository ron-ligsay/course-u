from django.db import models

from django.contrib.auth.models import User
from django.db.models import Max
from django.db import IntegrityError

from apps.website.models import Skill

# User Skill Model
class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} - {self.skill} - {self.level}"