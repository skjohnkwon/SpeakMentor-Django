from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class PracticeHistory(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    words = ArrayField(models.CharField(max_length=100, blank=True), default=list, blank=True)
    max_words = 10  

    def save(self, *args, **kwargs):
        if len(self.words) > self.max_words:
            self.words = self.words[-self.max_words:]
        super().save(*args, **kwargs)

class PracticeList(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    words = ArrayField(models.CharField(max_length=100, blank=True), default=list, blank=True)
    max_words = 10

    def save(self, *args, **kwargs):
        if len(self.words) > self.max_words:
            self.words = self.words[-self.max_words:]
        super().save(*args, **kwargs)

class ChatHistory(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    chat = models.JSONField()
    date = models.DateTimeField(auto_now_add=True)