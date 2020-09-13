# need to create some form of a user model, or use the default django user model
# have a match model for when two users match with eachother
# have a like model for when a user likes another
# when creating a follow, check if mutual, and if so create a match object
# could also create a head to head kind of model
# should get two and then when choosing a like, get two more
# keep track of the existing likes some way
# eventually will run out of possibilities
# should only be able to find roomates of the same gender and the same college
# should then be able to message possible roomates
# some kind of algorithm component to determine possible roomates
# send a request to get a new user no matter whether the previous one was liked or not
# make sure to check if the user has already been cycled through


from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Profile(models.Model):
    bio = models.CharField(max_length=500, default="")
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "profile")
    gender = models.CharField(max_length=20, default="")
    image = models.ImageField(upload_to='profile_pics',default="profile_pics/default-profile.jpg")

class Preferences(models.Model):
    loudness=models.CharField(max_length=20,default="")
    athleticism = models.CharField(max_length=20, default="")
    musicality = models.CharField(max_length=20, default="")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="preferences")
