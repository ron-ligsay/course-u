from django.db import models

from apps.recommender.models import UserRecommendations


class Survey(models.Model):
    recommendation = models.OneToOneField(UserRecommendations, on_delete=models.CASCADE, null=True)
    
    ques1 = models.CharField(
        max_length=100,
        choices=[('Undergraduate', 'Undergraduate'), ('Graduate', 'Graduate')],
        verbose_name='1. What is your current academic status?'
    )
    
    ques2 = models.CharField(
        max_length=100,
        choices=[
            ('IT', 'Information Technology'),
            ('CS', 'Computer Science'),
        ],
        verbose_name='2. What was your academic course during your studies?'
    )
    
    ques3 = models.CharField(
        max_length=100,
        choices=[
            ('1', 'Not Accurate'),
            ('2', 'Somewhat Accurate'),
            ('3', 'Neutral'),
            ('4', 'Accurate'),
            ('5', 'Very Accurate'),
        ],
        verbose_name='3. On a scale of 1 to 5, how accurate do you find the system''s'' recommendations in line with your academic interests and career goals? (1 - Not Accurate, 5 - Very Accurate)'
    )
    
    ques4 = models.CharField(
        max_length=100,
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No'),
        ],
        verbose_name='4. Have you encountered any challenges or discrepancies with the recommendations provided by the system?'
    )
    
    ques5 = models.CharField(
        max_length=100,
        choices=[
            ('Extremely Influential', 'Extremely Influential'),
            ('Moderately Influential', 'Moderately Influential'),
            ('Slightly Influential', 'Slightly Influential'),
            ('Not Influential at All', 'Not Influential at All'),
        ],
        verbose_name='5. To what extent do you feel the recommendation system has positively influenced your academic and career-related decisions?'
    )
    
    ques6 = models.CharField(
        max_length=100,
        choices=[
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
        ],
        verbose_name='6. On a scale of 1 to 5, how user-friendly do you find the recommendation system interface? (1 - Not User-Friendly, 5 - Very User-Friendly)'
    )

    ques7 = models.CharField(
        max_length=100,
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No'),
        ],
        verbose_name='7. Would you recommend this recommendation system to your peers or colleagues in IT/CS?'
    )

    ques7 = models.CharField(
        max_length=100,
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No'),
        ],
        verbose_name='7. Would you recommend this recommendation system to your peers or colleagues in IT/CS?'
    )



