from django.shortcuts import render
from .models import Follow, Match, UserOptionView
from .serializers import FollowSerializer, MatchSerializer, UserOptionViewSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.serializers import UserSerializer
import random

@api_view(['POST'])
def create_follow(request):
    matched = False
    serializer = FollowSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
    follower = request.data.get("follower", 0)
    followed = request.data.get("followed", 0)
    followed_follow_objects = list(followed.followed_objects.all())
    has_follower = list(filter(lambda follow: follow.followed == follower, followed_follow_objects))
    if len(has_follower):
        match = Match(first_user = follower, second_user = followed)
        match.save()
        matched = True
    return Response({'matched' : matched, 'data': serializer.data})

@api_view(['POST'])
def get_next_roommate(request):
    user = request.data.get("user", 0)
    # option_user = request.data.get("option", 0)
    # user_option_view = UserOptionView(user = user, option = option_user)
    # user_option_view.save()
    serializer = UserOptionViewSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
    possible_options = list(User.objects.all())
    user_viewed = list(user.already_viewed_options.all())

    new_option = possible_options[random.randint(0, len(possible_options))]
    while user_viewed.index(new_option) != -1:
        new_option = possible_options[random.randint(0, len(possible_options))]
    
    new_option_serializer = UserSerializer(data = new_option)
    return Response(new_option_serializer.data)

# May have a way to combine the two of these methods
# Combine so that the follow is a standard function not a view