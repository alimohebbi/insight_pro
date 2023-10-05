from datetime import timezone, datetime

from django.db import models

# Create your models here.

from django.db import models


class Company(models.Model):
    create_date = models.DateTimeField("date created", default=datetime.now())
    website_url = models.URLField(max_length=200, unique=True)
    topics = models.JSONField(default='')
    sentiment_score = models.FloatField()
    highlights = models.JSONField(null=True, blank=True, default='')
    word_cloud = models.ImageField(upload_to='word_clouds/', null=True)

    def __str__(self):
        return self.website_url


class Documents(models.Model):
    scrapped_documents = models.JSONField(null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
