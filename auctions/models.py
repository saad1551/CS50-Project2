from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_choices = [("fashion", "Fashion"), ("toys", "Toys"), ("electronics", "Electronics"), ("home", "Home")]
    name = models.CharField(choices=category_choices, unique=True, max_length=50)

class Listing(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    starting_bid = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    imageUrl = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings", blank=True, null=True)

    def __str__(self):
        return f"title: {self.title}\nstarting_bid={self.starting_bid}\ncategory:{self.category}"

class Bid(models.Model):
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid_amount = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")

class Comment(models.Model):
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")