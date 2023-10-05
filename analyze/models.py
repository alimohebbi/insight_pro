from datetime import timezone, datetime

import django
from django.db import models

# Create your models here.

from django.db import models


class Company(models.Model):
    create_date = models.DateTimeField("date created", default=django.utils.timezone.now)
    website_url = models.URLField(max_length=200, unique=True)
    domains = models.JSONField(default=dict)
    sentiment_score = models.FloatField()
    highlights = models.JSONField(null=True, blank=True, default=dict)
    word_cloud = models.ImageField(upload_to='word_clouds/', null=True)
    scrapped_documents = models.FileField(upload_to='documents', null=True)
    keywords = models.JSONField(null=True)
    def __str__(self):
        return self.website_url
