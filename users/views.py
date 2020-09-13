from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes, authentication_classes, permission_classes
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from .models import Profile, Message, User
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, ProfileSerializer, ProfileImageSerializer, ReplySerializer, MessageSerializer, CreateMessageSerializer, CreateReplySerializer
from rest_framework import status

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_profile(request):
    profile=Profile.objects.get(user=request.user)
    serializer = ProfileSerializer(
        profile, data=request.data, context={'request': request}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_gallery_image(request):
    serializer = ProfileImageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_inbox(request):
    messages= Message.objects.filter(recipient=request.user).order_by('-sent_at')
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_sent(request):
    messages= Message.objects.filter(sender=request.user).order_by('-sent_at')
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_message(request):
    serializer = CreateMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_reply(request):
    serializer = CreateReplySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_users(request):
    user = User.objects.get(pk = request.GET.get('pk', 1))
    user_matches_first = list(user.first_user_matches.all())
    user_matches_second = list(user.second_user_matches.all())
    logger.error(request.GET.get('pk', 0))
    logger.error(user_matches_second)
    users = []
    for um in user_matches_first:
        users.append(um.second_user)

    for um in user_matches_second:
        users.append(um.first_user)

    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)