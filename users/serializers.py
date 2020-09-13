from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Profile,  ProfileImage, Message, Reply

User._meta.get_field('email')._unique = True
class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields =('id', 'image','profile')
class ProfileSerializer(serializers.ModelSerializer):
    gallery_images = ProfileImageSerializer(many=True)
    class Meta:
        model = Profile
        fields = ('id','bio', 'gender', 'image',  'loudness', 'athleticism','musicality','university','gallery_images')

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile')
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
        )
        
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
class CreateReplySerializer(serializers.ModelSerializer):
    class Meta:
        model=Reply
        fields = ('id','sender', 'content', 'message')
class ReplySerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    class Meta:
        model=Reply
        fields = ('id','sender', 'content', 'message')
class MessageSerializer(serializers.ModelSerializer):
    message_replies=ReplySerializer(many=True)
    time_posted = serializers.ReadOnlyField(source='get_date')
    
    recipient=UserSerializer(read_only=True)
    sender=UserSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ('id', 'content','sender', 'recipient','time_posted', 'message_replies')

class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'content','sender', 'recipient')