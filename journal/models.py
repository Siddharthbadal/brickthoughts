from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Thought(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=300)

    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, max_length=20, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title


class Profile(models.Model):
    profile_pic = models.ImageField(null=True, blank=True, default="default.png")

    about = models.CharField(max_length=200, null=True, blank=True)
    place = models.CharField(max_length=100, null=True, blank=True)
    link = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, max_length=20, on_delete=models.CASCADE, default=1)
    thoughts = models.ForeignKey(Thought, related_name='userthought',on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.user.username