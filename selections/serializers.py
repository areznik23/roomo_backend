from rest_framework import serializers
from .models import Follow, Match, UserOptionView

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['pk', 'follower', 'followed', 'time_stamp']

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Match
        fields = ['pk', 'first_user', 'second_user', 'time_stamp']

class UserOptionViewSerializer(serializers.ModelSerializer):
    class Meta:
        model  = UserOptionView
        fields = ['pk', 'user', 'option', 'time_stamp']