from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    bio = models.CharField(max_length=500, default="")
    user = models.OneToOneField(User,  on_delete = models.CASCADE, related_name = "profile")
    gender = models.CharField(max_length=20, default="")
    image = models.ImageField(upload_to='profile_pics',default="profile_pics/default-profile.jpg")
    loudness=models.CharField(max_length=20,default="")
    athleticism = models.CharField(max_length=20, default="")
    musicality = models.CharField(max_length=20, default="")
    university = models.CharField(max_length=100, default="")

class ProfileImage(models.Model):
    image = models.ImageField(upload_to='gallery_images',default="profile_pics/default-profile.jpg")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="gallery_images")

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)



class Message(models.Model):
    content = models.TextField(max_length=500, default="")
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messages_sent")
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messages_received")
    sent_at = models.DateTimeField(auto_now_add=True)


    def get_date(self):
        time = timezone.now()
        if self.sent_at.day == time.day:
            if time.hour == self.sent_at.hour:
                if((time.minute - self.sent_at.minute) == 1):
                    return str(1) + " minute ago"
                return str(time.minute - self.sent_at.minute) + " minutes ago"
            else:
                if((time.hour - self.sent_at.hour) == 1):
                    return str(1) + " hour ago"
                return str(time.hour - self.sent_at.hour) + " hours ago"
        else:
            if self.sent_at.month == time.month:
                if((time.day - self.sent_at.day) == 1):
                    return str(1) + " day ago"
                return str(time.day - self.sent_at.day) + " days ago"
            else:
                if self.sent_at.year == time.year:
                    if((time.month - self.sent_at.month) == 1):
                        return str(1) + " month ago"
                    return str(time.month - self.sent_at.month) + " months ago"
        return self.sent_at
class Reply(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="message_replier")
    content = models.TextField(max_length=500, default="")
    message=models.ForeignKey(Message, on_delete=models.CASCADE, related_name="message_replies")
    