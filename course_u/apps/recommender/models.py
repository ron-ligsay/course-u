from django.db import models

from django.contrib.auth.models import User
from django.db.models import Max
from django.db import IntegrityError

from apps.website.models import Skill, Field

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


class UserRecommendations(models.Model):
    recommendation_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    selected_field = models.ForeignKey(Field, on_delete=models.CASCADE, null=True, blank=True)
    field_1 = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='field_1', null=True, blank=True)
    field_2 = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='field_2', null=True, blank=True)
    field_3 = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='field_3', null=True, blank=True)
    score_1 = models.FloatField(null=True, blank=True)
    score_2 = models.FloatField(null=True, blank=True)
    score_3 = models.FloatField(null=True, blank=True)
    current_year = models.PositiveIntegerField(null=True, blank=True, default=0)
    # You can add other fields here for additional information, such as scores, timestamps, etc.

    def __str__(self):
        return f"Recommendations for User: {self.user.username}"

    class Meta:
        ordering = ['user']  # Specify the default ordering for UserRecommendations
        unique_together = ('user', 'current_year')  # Ensure that each user has only one recommendation per field

