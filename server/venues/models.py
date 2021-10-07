from django.db import models

class Venue(models.Model):
    yelp_id = models.CharField(max_length=200, unique=True)
