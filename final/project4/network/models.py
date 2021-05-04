from django.contrib.auth.models import AbstractUser
from django.db import models

# base model included with dist


class User(AbstractUser):
    pass


# add post model
class Timer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    work_interval = models.IntegerField()
    rest_interval = models.IntegerField()

    def __str__(self):
        return "{self.user.username} -> {self.post}"

# add profile model


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{self.user.username}"
