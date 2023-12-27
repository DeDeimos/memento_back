from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.db.models import Q
from django.db.models import Count, Subquery, OuterRef
from .models import User, Moment, Comment, Like, Follow, Tag
from .serializers import UserFollowingMomentSerializer, UserFollowingMomentSerializer, MomentStatisticSerializer, UserLoginSerializer, UserRegisterSerializer, UserSerializer, MomentSerializer, CommentSerializer, LikeSerializer, FollowSerializer, TagSerializer
from cent import Client
from django.http import JsonResponse
from rest_framework.pagination import LimitOffsetPagination
# from django.apps import AppConfig
# from .signals import send_subscription_notification

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

class UserChangePassword(APIView):
    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('pk')
        new_password = self.request.data.get('new_password')

        # Проверка, что user_id и new_password переданы
        if not user_id or not new_password:
            return Response({'error': 'User ID and new password are required.'}, status=400)

        user = get_object_or_404(User, pk=user_id)

        # Изменение пароля
        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password changed successfully.'})
    
class UserChangeNameandEmail(APIView):
    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('pk')
        new_name = self.request.data.get('new_name')
        new_email = self.request.data.get('new_email')

        # Проверка, что user_id, new_name и new_email переданы
        if not user_id or not new_name or not new_email:
            return Response({'error': 'User ID, new name, and new email are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = get_object_or_404(User, pk=user_id)
            user.set_name_email(new_name, new_email)
            return Response({'message': 'Name and email changed successfully.'})
        except IntegrityError as e:
            error_message = str(e)
            if 'unique constraint' in error_message.lower():
                if 'email' in error_message.lower():
                    return Response({'error': 'Email is not unique.'}, status=status.HTTP_400_BAD_REQUEST)
                elif 'name' in error_message.lower():
                    return Response({'error': 'Name is not unique.'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'error': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({'error': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UserChangeProfilePhoto(APIView):
    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('pk')
        new_profile_photo = self.request.data.get('new_profile_photo')

        # Проверка, что user_id и new_profile_photo переданы
        if not user_id or not new_profile_photo:
            return Response({'error': 'User ID and new profile photo are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, pk=user_id)

        # Изменение профильной фотографии
        user.profilephoto = new_profile_photo
        user.save()

        return Response({'message': 'Profile photo changed successfully.'}, status=status.HTTP_200_OK)
    

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
    serializer_class = UserFollowingMomentSerializer

    def get_object(self):
        user_id = self.kwargs['user_id']
        moment_id = self.kwargs['moment_id']
        
        # Проверка существования пользователя и момента
        if not Follow.objects.filter(follower=user_id).exists():
            return None

        following_users = Follow.objects.filter(follower=user_id).values('following')
        moment = Moment.objects.filter(pk=moment_id, author__in=following_users).first()

        return moment

    def get_serializer_context(self):
        # Передача user_id и других контекстных данных сериализатору
        return {'user_id': self.kwargs['user_id']}

class MomentByUser(generics.ListAPIView):
    serializer_class = MomentSerializer

    def get_queryset(self):
        queryset = Moment.objects.all()
        user_id = self.kwargs['pk']
        return queryset.filter(author=user_id) 

class MomentStatistic(APIView):
    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        user = User.objects.filter(pk=user_id).first()

        if not user:
            return Response({'error': 'User not found'}, status=404)

        moment_id = self.kwargs.get('pk')
        moment = Moment.objects.filter(pk=moment_id).first()

        if not moment:
            return Response({'error': 'Moment not found'}, status=404)

        # Получаем значение параметра comment_count из запроса
        comment_count_param = request.query_params.get('comment_count')
        
        if comment_count_param is not None:
            try:
                comment_count = int(comment_count_param)
            except ValueError:
                return Response({'error': 'Invalid comment_count value. Must be an integer.'}, status=400)

            recent_comments = Comment.objects.filter(moment=moment).order_by('-created_at')[:comment_count]
        else:
            recent_comments = Comment.objects.filter(moment=moment).order_by('-created_at')

        comment_data = []
        for comment in recent_comments:
            has_user_liked = Like.objects.filter(author=user, comment=comment).exists()

            comment_data.append({
                'id': comment.id,
                'text': comment.text,
                'created_at': comment.created_at,
                'author': {
                    'id': comment.author.id,
                    'name': comment.author.name,
                },
                'has_user_liked': has_user_liked,
            })

        data = {
            'like_count': Like.objects.filter(moment=moment).count(),
            'recent_comments': comment_data,
        }

        return Response(data)
    
# ����� 20 ����� ���������� �������� �� �������� ������������� ����� ����� �� ������������ ��������� memcached
# @method_decorator(cache_page(60 * 15, key_prefix='popular_moments'), name='get')
# class MomentPopular(generics.ListAPIView):
#     queryset = Moment.objects.all()[:20]
#     serializer_class = MomentSerializer
    
#     @method_decorator(cache_page(60 * 15, key_prefix='popular_moments'), name='get')
#     def get(self, request, *args, **kwargs):
#         return super().get(request, *args, **kwargs)

#     def update_cache(self):
#         # ������� ��� �� �����
#         cache.delete('popular_moments')

#     def perform_update(self, serializer):
#         # ��������� ���������� ������� � ���� ������
#         instance = serializer.save()
#         # �������� ����� ���������� ����
#         self.update_cache()

class MomentPopular(generics.ListAPIView):
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        # Ваш текущий код для получения моментов
        moments = Moment.objects.all()[:20]
        return moments

    def get_serializer_class(self):
        # Используйте ваш пользовательский сериализатор здесь
        return UserFollowingMomentSerializer

    def update_cache(self):
        # Ваш текущий код для обновления кеша
        cache.delete('popular_moments')

    def perform_update(self, serializer):
        # Ваш текущий код для обновления момента
        instance = serializer.save()
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
    
# class FollowCreate(generics.CreateAPIView):
#     queryset = Follow.objects.all()
#     serializer_class = FollowSerializer

#     def perform_create(self, serializer):
#         instance = serializer.save()
#         send_subscription_notification(instance.follower.id, instance.following.id)


class FollowEdit(generics.RetrieveUpdateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

class FollowDelete(generics.DestroyAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    
    def get_object(self):
        follower_id = self.kwargs.get('id_follower')
        following_id = self.kwargs.get('id_following')
        return Follow.objects.get(follower=follower_id, following=following_id)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Подписка успешно отменена'}, status=status.HTTP_200_OK)

    

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

# class UserFollowingMoments(generics.ListAPIView):
#     serializer_class = UserFollowingMomentSerializer

#     def get_queryset(self):
#         user_id = self.kwargs['pk']
#         following_users = Follow.objects.filter(follower=user_id).values('following')
#         moments = Moment.objects.filter(author__in=following_users).order_by('-created_at')

#         return moments

#     def get_serializer_context(self):
#         # ��������� user_id � ��������� �������������
#         return {'user_id': self.kwargs['pk']}

class UserFollowingMoments(generics.ListAPIView):
    serializer_class = UserFollowingMomentSerializer

    def get_queryset(self):
        user_id = self.kwargs['pk']
        following_users = Follow.objects.filter(follower=user_id).values('following')
        
        # Получение параметров limit и offset из запроса
        limit = int(self.request.query_params.get('limit', 10))
        offset = int(self.request.query_params.get('offset', 0))

        # Применение limit и offset к запросу
        moments = Moment.objects.filter(author__in=following_users).order_by('-created_at')[offset:offset + limit]

        return moments

    def get_serializer_context(self):
        # Передача user_id и других контекстных данных сериализатору
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

class TagByMoment(generics.ListAPIView):
    serializer_class = TagSerializer

    def get_queryset(self):
        queryset = Tag.objects.all()
        moment_id = self.kwargs['pk']
        return queryset.filter(moment=moment_id)

#Поиск через query_params моментов по тегу и пользотелей по имени
class Search(APIView):
    def get(self, request, format=None):
        query = request.query_params.get('query')
        
        if not query:
            return Response({'moments': [], 'users': []}, status=status.HTTP_200_OK)

        momentQuerySet = Moment.objects.filter(Q(tag__name__icontains=query)).distinct()
        userQuerySet = User.objects.filter(name__icontains=query)
        
        momentSerializer = MomentSerializer(momentQuerySet, many=True)
        userSerializer = UserSerializer(userQuerySet, many=True)
        
        return Response({'moments': momentSerializer.data, 'users': userSerializer.data}, status=status.HTTP_200_OK)
    
cent = Client(address="185.204.2.233:8111")

def send_like_notification(user_id, moment_id, recipient_user_id):
    channel_name = f'like_channel_{recipient_user_id}'
    data = {
        'event': 'like',
        'user_id': user_id,
        'moment_id': moment_id,
    }
    cent.publish(channel_name, data)

# def send_subscription_notification(follower_id, following_id):
#     channel_name = f'subscription_channel_{following_id}'
#     data = {
#         'event': 'subscription',
#         'follower_id': follower_id,
#         'following_id': following_id,
#         'message': f'Пользователь {follower_id} подписался на вас.',
#     }
#     cent.publish(channel_name, data)
#     notifications_channel_name = 'notifications'
#     cent.publish(notifications_channel_name, data)

# def like_view(request, moment_id, recipient_user_id):
#     # Обработка лайка
#     # ...
#     send_like_notification(request.user.id, moment_id, recipient_user_id)
#     return JsonResponse({'status': 'success'})

# def subscription_view(request, following_id):
#     # Обработка подписки
#     # ...
#     send_subscription_notification(request.user.id, following_id)
#     return JsonResponse({'status': 'success'})

# class YourAppConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'your_app'

#     def ready(self):
#         import api.signals