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

class UserSkillSource(models.Model):
    user_skill = models.ForeignKey(UserSkill, on_delete=models.CASCADE)  # Link to the UserSkill instance
    source_type = models.CharField(max_length=50)  # The type of source (e.g., 'test', 'personality', 'subject')
    source_id = models.PositiveIntegerField()  # The ID of the specific source (e.g., the test ID, personality type ID, or subject ID)

    def __str__(self):
        return f"{self.user_skill.user.username}'s {self.user_skill.skill.name} source from {self.source_type} {self.source_id}"