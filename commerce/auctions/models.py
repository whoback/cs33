from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.category}"


class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=6, decimal_places=2)
    current_bid = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField()
    date_listed = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listed_by = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, related_name='listings', blank=True, null=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=True)


class Comment(models.Model):
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.TextField()


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    watch_bool = models.BooleanField(default=True)


class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self) -> str:
        return f"user: {self.user}, bid: {self.bid}"
