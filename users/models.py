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



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

""" class Message(models.Model):
	giver = models.ForeignKey(User, on_delete = models.CASCADE, related_name="sent_messages")
	receiver = models.ForeignKey(User, on_delete = models.CASCADE, related_name="received_messages")
	time_stamp = models.DateTimeField(auto_now_add = True)
	message = models.CharField(max_length=200, default="")

	def get_date(self):
		time = timezone.now()
		if self.time_stamp.day == time.day:
			if time.hour==self.time_stamp.hour:
				if((time.minute - self.time_stamp.minute)==1):
					return str(1) + " minute ago"
				return str(time.minute - self.time_stamp.minute) + " minutes ago"
			else:
				if((time.hour - self.time_stamp.hour)==1):
					return str(1) + " hour ago"
				return str(time.hour - self.time_stamp.hour) + " hours ago"
		else:
			if self.time_stamp.month == time.month:
				if((time.day - self.time_stamp.day)==1):
					return str(1) + " day ago"
				return str(time.day - self.time_stamp.day) + " days ago"
			else:
				if self.time_stamp.year == time.year:
					if((time.month - self.time_stamp.month)==1):
						return str(1) + " month ago"
					return str(time.month - self.time_stamp.month) + " months ago"
		return self.time_stamp """