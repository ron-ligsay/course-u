from django.db import models

class Survey(models.Model):
    q1 = models.CharField(
        max_length=100,
        choices=[('IT', 'Information Technology'), ('CS', 'Computer Science')],
        verbose_name='1. What was your academic specialization?'
    )
    
    q2 = models.CharField(
        max_length=100,
        choices=[
            ('Completely Aligned', 'Completely Aligned'),
            ('Mostly Aligned', 'Mostly Aligned'),
            ('Somewhat Aligned', 'Somewhat Aligned'),
            ('Not Aligned at All', 'Not Aligned at All'),
        ],
        verbose_name='2. To what extent do you feel your academic specialization aligns with your current job responsibilities?'
    )
    
    q3 = models.CharField(
        max_length=100,
        choices=[
            ('Very Well', 'Very Well'),
            ('Well', 'Well'),
            ('Neutral', 'Neutral'),
            ('Poorly', 'Poorly'),
            ('Not at All', 'Not at All'),
        ],
        verbose_name='3. How well did your academic specialization prepare you for your current role?'
    )
    
    q4 = models.BooleanField(
        verbose_name='4. Have you pursued any additional certifications or training after graduation to enhance your skills for your current job?'
    )
    
    q5 = models.CharField(
        max_length=100,
        choices=[('Yes', 'Yes'), ('No', 'No'), ('Not Sure', 'Not Sure')],
        verbose_name='5. In hindsight, do you think a different academic specialization might have better prepared you for your current career?'
    )
    
    q6 = models.CharField(
        max_length=100,
        choices=[
            ('Very Satisfied', 'Very Satisfied'),
            ('Satisfied', 'Satisfied'),
            ('Neutral', 'Neutral'),
            ('Dissatisfied', 'Dissatisfied'),
            ('Very Dissatisfied', 'Very Dissatisfied'),
        ],
        verbose_name='6. How satisfied are you with your current job in terms of alignment with your academic specialization and overall career growth?'
    )