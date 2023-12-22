from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.db.models import Count, Subquery, OuterRef
from .models import User, Moment, Comment, Like, Follow, Tag
from .serializers import UserFollowingMomentSerializer, UserFollowingMomentSerializer, MomentStatisticSerializer, UserLoginSerializer, UserRegisterSerializer, UserSerializer, MomentSerializer, CommentSerializer, LikeSerializer, FollowSerializer, TagSerializer

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
                return Response({'id': user.id, 'message': 'РђРІС‚РѕСЂРёР·Р°С†РёСЏ СѓСЃРїРµС€РЅР°'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'РќРµРїСЂР°РІРёР»СЊРЅС‹Рµ СѓС‡РµС‚РЅС‹Рµ РґР°РЅРЅС‹Рµ'}, status=status.HTTP_401_UNAUTHORIZED)
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

class MomentStatistic(APIView):
    def get(self, request, *args, **kwargs):
        moments = Moment.objects.all()

        # Получение данных о статистике для каждого момента
        data = []
        for moment in moments:
            like_count = Like.objects.filter(moment=moment).count()
            recent_comments = Comment.objects.filter(moment=moment).order_by('-created_at').values_list('text', flat=True)[:2]

            moment_data = {
                'id': moment.id,
                'like_count': like_count,
                'recent_comments': list(recent_comments),
            }

            data.append(moment_data)

        return Response(data)

# Взять 20 самых популярных моментов по рейтингу пользователей чтобы потом их закешировать используя memcached
@method_decorator(cache_page(60 * 15, key_prefix='popular_moments'), name='get')
class MomentPopular(generics.ListAPIView):
    queryset = Moment.objects.all()[:20]
    serializer_class = MomentSerializer
    
    @method_decorator(cache_page(60 * 15, key_prefix='popular_moments'), name='get')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def update_cache(self):
        # Очищаем кэш по ключу
        cache.delete('popular_moments')

    def perform_update(self, serializer):
        # Выполняем обновление объекта в базе данных
        instance = serializer.save()
        # Вызываем метод обновления кэша
        self.update_cache()

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

    def get_object(self):
        author_id = self.kwargs.get('id_author')
        moment_id = self.kwargs.get('id_moment')
        comment_id = self.kwargs.get('id_comment')
        like_type = self.request.data.get('type')

        if like_type == 'moment':
            obj = Like.objects.filter(author_id=author_id, moment_id=moment_id).first()
        elif like_type == 'comment':
            obj = Like.objects.filter(author_id=author_id, comment_id=comment_id).first()
        else:
            obj = None

        if obj is None:
            raise generics.NotFound("Like not found")

        return obj

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


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

# class UserFollowingMoments(generics.ListAPIView):
#     serializer_class = UserFollowingMomentSerializer

#     def get_queryset(self):
#         user_id = self.kwargs['pk']
#         following_users = Follow.objects.filter(follower=user_id).values('following')
#         queryset = Moment.objects.filter(author__in=following_users)
#         return queryset[::-1]

class UserFollowingMoments(generics.ListAPIView):
    serializer_class = UserFollowingMomentSerializer

    def get_queryset(self):
        user_id = self.kwargs['pk']
        following_users = Follow.objects.filter(follower=user_id).values('following')
        moments = Moment.objects.filter(author__in=following_users).order_by('-created_at')

        return moments

    def get_serializer_context(self):
        # Передайте user_id в контексте сериализатора
        return {'user_id': self.kwargs['pk']}

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

    