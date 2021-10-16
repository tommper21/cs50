from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return self.category


class Listing(models.Model):
    owner =       models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    title =       models.CharField(max_length=64)
    description = models.CharField(max_length=2000)
    category =    models.CharField(max_length=64, default="None")
    image =       models.URLField(max_length=10000)
    price =       models.IntegerField()
    date =        models.DateTimeField(auto_now_add=True)
    active =      models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item")
    user =    models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    bid =     models.IntegerField()

    def __str__(self):
        return f"{self.user} bids {self.bid} on {self.listing}!"


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="commented_listing")
    user =    models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    comment = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user} commented {self.comment} on {self.listing}"

class Watchlist(models.Model):
    user =    models.ForeignKey(User, on_delete=models.CASCADE, related_name="current_user")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="current_listing")


    def __str__(self):
        return f"{self.listing} is on the watchlist of {self.user}"
