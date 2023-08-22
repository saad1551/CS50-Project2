from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField
    starting_bid = models.FloatField

class Bid(models.Model):
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid_amount = models.FloatField
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")

class Comment(models.Model):
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")