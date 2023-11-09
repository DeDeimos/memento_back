from rest_framework import serializers
from .models import User, Moment, Comment, Like, Follow, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password', 'profilephoto', 'created_at', 'rating')

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password', 'profilephoto')
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['name'], validated_data['email'], validated_data['password'])
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    def check_user(self, validated_data):
        user = User.objects.get(email=validated_data['email'])
        print(user)
        print("check login")
        if user.check_password(validated_data['password']):
            return user
        else:
            return None
    class Meta:
        model = User
        fields = ('id', 'email', 'password')

class MomentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moment
        fields = ('id', 'author', 'description', 'image', 'created_at')

class UserFollowingMomentSerializer(serializers.ModelSerializer):
    author_info = UserSerializer(source='author', read_only=True)

    class Meta:
        model = Moment
        fields = ('id', 'author_info', 'description', 'image', 'created_at')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'author', 'moment', 'text', 'created_at') 

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'author', 'moment', 'comment', 'created_at')

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('id', 'follower', 'following', 'created_at')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'moment')

