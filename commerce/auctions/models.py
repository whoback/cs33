from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=6, decimal_places=2)
    current_bid = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField()
    date_listed = models.DateTimeField()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listed_by = models.CharField(max_length=255)


class Comment(models.Model):
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
