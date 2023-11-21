from django.db import models
from datetime import date
from apps.website.models import Field

# Create your models here.
# link,keyword,title,company,company_link,date
class JobPosting(models.Model):
    link = models.CharField(max_length=5000)
    keyword = models.CharField(max_length=100)
    #keyword_id = models.IntegerField(blank=True, null=True)
    field = models.ForeignKey(Field, on_delete=models.CASCADE, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=100)
    company_link = models.CharField(max_length=5000)
    #description = models.TextField()
    #requirements = models.TextField()
    date_posted = models.DateField()#default=date.today/auto_now_add=True
    location = models.CharField(max_length=300, blank=True, null=True)
    employment_type = models.CharField(max_length=150, blank=True, null=True)
    job_function = models.CharField(max_length=150, blank=True, null=True)
    industries = models.CharField(max_length=150, blank=True, null=True)
    seniority_level = models.CharField(max_length=150, blank=True, null=True)
    # job description with html tags
    job_description = models.TextField( blank=True, null=True)

    def __str__(self):
        return self.job_title