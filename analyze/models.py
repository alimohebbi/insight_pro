from datetime import timezone, datetime

from django.db import models

# Create your models here.

from django.db import models


class Insight(models.Model):
    create_date = models.DateTimeField("date created", default=datetime.now())
    website_url = models.URLField(max_length=200)
    topics = models.JSONField(default='')
    sentiment_score = models.FloatField()
    highlights = models.JSONField(null=True, blank=True, default='')
    scrapped_text = models.TextField(default='')

    def __str__(self):
        return self.website_url
