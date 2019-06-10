from django.db import models
from django.utils import timezone


class User(models.Model):
    name = models.CharField(max_length=200)
    is_active = models.BooleanField()
    fb_user_id = models.CharField(max_length=50)
    fb_token = models.TextField()

    def deactivate(self):
        self.is_active = False
        self.fb_token = ''
        self.fb_user_id = ''
        self.save()
        history = UserHistory(user=self, action=False, datetime=timezone.now())
        history.save()

    def activate(self):
        self.is_active = True
        self.save()
        history = UserHistory(user=self, action=True, datetime=timezone.now())
        history.save()
        pass


class UserHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    action = models.BooleanField(help_text='True signup/login, False deauth')
    datetime = models.DateTimeField()
