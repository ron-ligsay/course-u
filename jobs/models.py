from django.db import models
from datetime import date

# Create your models here.
# link,keyword,title,company,company_link,date
class JobPosting(models.Model):
    link_clean = models.CharField(max_length=5000)
    keyword = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    company_link = models.CharField(max_length=1000)
    #description = models.TextField()
    #requirements = models.TextField()
    date_posted = models.DateField()#default=date.today/auto_now_add=True

    def __str__(self):
        return self.title