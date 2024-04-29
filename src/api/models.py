from django.db import models
from django.contrib.postgres.fields import ArrayField
from collections import OrderedDict
from django.utils import timezone

class ChatHistory(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    chat = models.JSONField()
    date = models.DateTimeField(auto_now_add=True)

class Questionnaire(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    birth_year = models.PositiveIntegerField()
    native_language = models.CharField(max_length=100)
    years_speaking_english = models.PositiveIntegerField()
