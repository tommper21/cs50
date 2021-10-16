from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return self.username


class Post(models.Model):
    owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="creator")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)


    def serialize(self):
        return {
            "id": self.id,
            "owner": self.owner.username,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            "likes": self.likes
        }

    def __str__(self):
        return self.body

class Follow(models.Model):
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="who_follows")
    followed = models.ForeignKey("User", on_delete=models.CASCADE, related_name="who_gets_followed")

    def __str__(self):
        return f"{self.folllower} follows {self.followed}"


class Like(models.Model):
    liker = models.ForeignKey("User", on_delete=models.CASCADE, related_name="someone_likes")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="gets_liked")

    def __str__(self):
        return f"{self.liker} likes {self.post}"
