from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Moment, Comment, Like, Follow, Tag
from .serializers import UserFollowingMomentSerializer, UserLoginSerializer, UserRegisterSerializer, UserSerializer, MomentSerializer, CommentSerializer, LikeSerializer, FollowSerializer, TagSerializer
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# Create your views here.
#User
class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserEdit(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDelete(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRegister(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

class UserLogin(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.check_user(serializer.validated_data)
            print(user)
            if user:
                return Response({'id': user.id, 'message': 'Авторизация успешна'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Неправильные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Moment
class MomentView(generics.ListAPIView):
    queryset = Moment.objects.all()
    serializer_class = MomentSerializer

class MomentCreate(generics.CreateAPIView):
    queryset = Moment.objects.all()
    serializer_class = MomentSerializer

class MomentEdit(generics.RetrieveUpdateAPIView):
    queryset = Moment.objects.all()
    serializer_class = MomentSerializer

class MomentDelete(generics.DestroyAPIView):
    queryset = Moment.objects.all()
    serializer_class = MomentSerializer

class MomentDetail(generics.RetrieveAPIView):
    queryset = Moment.objects.all()
    serializer_class = MomentSerializer

class MomentByUser(generics.ListAPIView):
    serializer_class = MomentSerializer

    def get_queryset(self):
        queryset = Moment.objects.all()
        user_id = self.kwargs['pk']
        return queryset.filter(author=user_id) 

#Comment
class CommentView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentCreate(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentEdit(generics.RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentDelete(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentDetail(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

#Like
class LikeView(generics.ListAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

class LikeCreate(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

class LikeEdit(generics.RetrieveUpdateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

class LikeDelete(generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

class LikeDetail(generics.RetrieveAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

#Follow
class FollowView(generics.ListAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

class FollowCreate(generics.CreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

class FollowEdit(generics.RetrieveUpdateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

class FollowDelete(generics.DestroyAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

class FollowDetail(generics.RetrieveAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

class UserFollow(generics.ListAPIView):
    serializer_class = FollowSerializer

    def get_queryset(self):
        queryset = Follow.objects.all()
        user_id = self.kwargs['pk']
        return queryset.filter(follower=user_id)

class UserFollowed(generics.ListAPIView):
    serializer_class = FollowSerializer

    def get_queryset(self):
        queryset = Follow.objects.all()
        user_id = self.kwargs['pk']
        return queryset.filter(following=user_id)

class UserFollowingMoments(generics.ListAPIView):
    serializer_class = UserFollowingMomentSerializer

    def get_queryset(self):
        user_id = self.kwargs['pk']
        following_users = Follow.objects.filter(follower=user_id).values('following')
        queryset = Moment.objects.filter(author__in=following_users)
        return queryset[::-1]


#Tag
class TagView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TagCreate(generics.CreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TagEdit(generics.RetrieveUpdateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TagDelete(generics.DestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TagDetail(generics.RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    