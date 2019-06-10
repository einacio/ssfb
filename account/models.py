from django.db import models


class User(models.Model):
    name = models.CharField(max_length=200)
    is_active = models.BooleanField()
    fb_user_id = models.CharField(max_length=50)
    fb_token = models.TextField()


class UserHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    action = models.BooleanField(help_text='True signup/login, False deauth')
    datetime = models.DateTimeField()
