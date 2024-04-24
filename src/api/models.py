from django.db import models
from django.contrib.postgres.fields import ArrayField
from collections import OrderedDict
from django.utils import timezone

class PracticeHistory(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    words = ArrayField(models.CharField(max_length=100, blank=True), default=list, blank=True)
    max_words = 10  

    def save(self, *args, **kwargs):
        unique_words = list(OrderedDict.fromkeys(self.words))
        if len(unique_words) > self.max_words:
            unique_words = unique_words[-self.max_words:]
        self.words = unique_words
        super().save(*args, **kwargs)

class PracticeList(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    words = ArrayField(models.CharField(max_length=100, blank=True), default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class ChatHistory(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    chat = models.JSONField()
    date = models.DateTimeField(auto_now_add=True)

class Questionnaire(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    native_language = models.CharField(max_length=100)
    years_speaking_english = models.PositiveIntegerField()
