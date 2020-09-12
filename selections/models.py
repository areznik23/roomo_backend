from django.db import models
from django.contrib.auth.models import User

class Follow(models.Model):
    followed = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "followed_objects")
    follower = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "follower_objects")
    time_stamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.follower.username + ": " + self.followed.username

# The related name situation for this model is a bit tricky
# Have to get the objects for when the user is first or when second
# Create some function to retreive all of the match objects for a given user
class Match(models.Model):
    first_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "first_user_matches")
    second_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "second_user_matches")
    time_stamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.first_user.username + ": " + self.second_user.username

class UserOptionView(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "already_viewed_options")
    option = models.ForeignKey(User, on_delete = models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return "User Option View: user - " + self.user.username + " - option - " + self.option.username 
