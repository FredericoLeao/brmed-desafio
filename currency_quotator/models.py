from django.db import models


class CurrencyRate(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField(null=False, blank=False, unique=True)
    base = models.CharField(max_length=5)
    rates = models.TextField()

