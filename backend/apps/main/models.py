from django.db import models
from django.contrib.postgres.search import TrigramSimilarity

class Location(models.Model):
    normalized_address = models.TextField(unique=True)
    formatted_address = models.TextField()
    lat = models.DecimalField(max_digits=10, decimal_places=8)
    lng = models.DecimalField(max_digits=11, decimal_places=8)

    def __str__(self):
        return self.formatted_address
