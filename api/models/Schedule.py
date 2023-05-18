from django.db import models

from .User import User


class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry_datetime = models.DateTimeField()
    exit_datetime = models.DateTimeField(null=True, blank=True)