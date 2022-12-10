from django.db import models
from django.conf import settings

class Shopping(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
    date = models.DateField()
    place = models.CharField(max_length=50)
    bought = models.CharField(max_length=1000)