from django.contrib.auth.models import AbstractUser
from django.db import models

# base model included with dist


class User(AbstractUser):
    pass


# add post model
class Timer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    work_interval = models.IntegerField()
    rest_interval = models.IntegerField()
    repititions = models.IntegerField(default=1)
    sound = models.CharField(max_length=500, null=True, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "work_interval": self.work_interval,
            "rest_interval": self.rest_interval,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }

# add profile model


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{self.user.username}"
