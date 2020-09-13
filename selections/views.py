from django.shortcuts import render
from .models import Follow, Match, UserOptionView
from .serializers import FollowSerializer, MatchSerializer, UserOptionViewSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.serializers import UserSerializer
import random


# Have to sort out the proper users count element, make sure cycling through all of the users

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@api_view(['POST'])
def create_follow(request):
    matched = False
    serializer = FollowSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
    follower = request.data.get("follower", 0)
    followed = request.data.get("followed", 0)
    followed_follow_objects = list(followed.followed_objects.all())
    has_follower = []
    for followed_follow_object in followed_follow_objects:
        if followed_follow_object.followed == follower:
            has_follower.append(followed_follow_object.followed)
    if len(has_follower) > 0:
        match = Match(first_user = follower, second_user = followed)
        match.save()
        matched = True
    return Response({'matched' : matched, 'data': serializer.data})

def get_match(follower, followed):
    matched = False
    follow = Follow(follower = follower, followed = followed)
    follow.save()

    followed_follow_objects = list(followed.follower_objects.all())
    logger.error(followed_follow_objects)
    has_follower = []
    for followed_follow_object in followed_follow_objects:
        if followed_follow_object.followed == follower:
            has_follower.append(followed_follow_object.followed)
   
    if len(has_follower) > 0:
        match = Match(first_user = follower, second_user = followed)
        match.save()
        matched = True

    serializer = FollowSerializer(follow)
    return {'match' : matched, 'follow': serializer.data}

@api_view(['POST'])
def get_next_roommate(request):
    user = User.objects.get(pk = request.data.get("follower", {})["user"]["id"])
    user_viewed = list(user.already_viewed_options.all())
    option_user = User.objects.get(pk = request.data.get("followed", {})["id"])

    if not((request.data.get("followed", {})["id"] == 1 and len(user_viewed) == 0) or option_user == user):
        user_option_view = UserOptionView(user = user, option = option_user)
        user_option_view.save()

    possible_options = list(User.objects.all())
    possible_options.remove(user)
    user_viewed_users = []
    for user_view in user_viewed:
        user_viewed_users.append(user_view.option)

    new_option = possible_options[random.randint(0, len(possible_options) - 1)]
    users_count = 1

    no_more_options = False
    while is_in_list(user_viewed_users, new_option, user):
        new_option = possible_options[random.randint(0, len(possible_options) - 1)]
        users_count += 1
        if users_count >= len(possible_options):
            no_more_options = True
            new_option = None
            break

    new_option_serializer = UserSerializer(new_option)

    return Response({'new_option': new_option_serializer.data, 'data': get_match(user, option_user), 'empty' : no_more_options})

@api_view(['POST'])
def get_next_roommate_no_follow(request):
    user = User.objects.get(pk = request.data.get("follower", {})["user"]["id"])
    user_viewed = list(user.already_viewed_options.all())
    option_user = User.objects.get(pk = request.data.get("followed", 1)["id"])

    if not((request.data.get("followed", {})["id"] == 1 and len(user_viewed) == 0) or option_user == user):
        user_option_view = UserOptionView(user = user, option = option_user)
        user_option_view.save()

    possible_options = list(User.objects.all())
    possible_options.remove(user)
    user_viewed_users = []
    for user_view in user_viewed:
        user_viewed_users.append(user_view.option)

    new_option = possible_options[random.randint(0, len(possible_options) - 1)]
    users_count = 1

    no_more_options = False
    while is_in_list(user_viewed_users, new_option, user):
        new_option = possible_options[random.randint(0, len(possible_options) - 1)]
        users_count += 1
        if users_count >= len(possible_options):
            no_more_options = True
            new_option = None
            break
    
    new_option_serializer = UserSerializer(new_option)

    return Response({'new_option': new_option_serializer.data, 'data':  {'match' : False, 'follow': None}, 'empty' : no_more_options})

@api_view(['GET'])
def get_initial_option(request):
    user = User.objects.get(pk = request.GET.get('pk', 0))
    possible_options = list(User.objects.all())
    user_viewed = list(user.already_viewed_options.all())

    new_option = possible_options[random.randint(0, len(possible_options) - 1)]
    while is_in_list(user_viewed, new_option, user):
        new_option = possible_options[random.randint(0, len(possible_options) - 1)]
    
    new_option_serializer = UserSerializer(new_option)
    return Response(new_option_serializer.data)

def is_in_list(options, element, user):
    try:
        index = options.index(element)
    except ValueError:
        return False
    return True

# May have a way to combine the two of these methods
# Combine so that the follow is a standard function not a view