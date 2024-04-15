from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class UserData(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    sub_plan = models.CharField(max_length=100, default='free')
    practice_list = models.ForeignKey('api.practicelist', on_delete=models.CASCADE, blank=True, null=True)
    chat_history = models.ForeignKey('api.chathistory', on_delete=models.CASCADE, blank=True, null=True)

class PracticeHistory(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    words = ArrayField(models.CharField(max_length=100, blank=True), default=list, blank=True)

class PracticeList(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    words = ArrayField(models.CharField(max_length=100, blank=True), default=list, blank=True)

class ChatHistory(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    chat = models.JSONField()
    date = models.DateTimeField(auto_now_add=True)