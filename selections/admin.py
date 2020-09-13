from django.contrib import admin
from .models import Follow, Match, UserOptionView

admin.site.register(UserOptionView)
admin.site.register(Follow)
admin.site.register(Match)
