from django.contrib import admin
from .models import Profile, ProfileImage,Message
# Register your models here.
class ProfileImageAdmin(admin.StackedInline):
    model = ProfileImage
 
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = [ProfileImageAdmin]
 
    class Meta:
       model = Profile
 
@admin.register(ProfileImage)
class ProfileImageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Message)
