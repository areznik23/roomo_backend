from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Preferences(models.Model):
    loudness=models.CharField(max_length=20,default="")
    



class Profile(models.Model):
    bio = models.CharField(max_length=500, default="")
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "profile")
    gender = models.CharField(max_length=20, default="")
    image = models.ImageField(upload_to='profile_pics',default="profile_pics/default-profile.jpg")
    preferences=models.ForeignKey(Preferences, on_delete=models.CASCADE, related_name="preferences")
