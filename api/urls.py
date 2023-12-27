from django.urls import path
from django.views.decorators.cache import cache_page
from .views import MomentByUser, MomentStatistic, MomentPopular, Search, TagByMoment, UserChangeNameandEmail, UserChangePassword, UserChangeProfilePhoto, UserFollow, UserFollowed, UserFollowingMoments, UserLogin, UserView, UserCreate, UserEdit, UserDelete, UserDetail, MomentView, MomentCreate, MomentEdit, MomentDelete, MomentDetail, CommentView, CommentCreate, CommentEdit, CommentDelete, CommentDetail, LikeView, LikeCreate, LikeEdit, LikeDelete, LikeDetail, FollowView, FollowCreate, FollowEdit, FollowDelete, FollowDetail, TagView, TagCreate, TagEdit, TagDelete, TagDetail
urlpatterns = [
    path('users/', UserView.as_view()),
    path('users/create', UserCreate.as_view()),
    path('users/edit/<int:pk>/', UserEdit.as_view()),
    path('users/delete/<int:pk>/', UserDelete.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('users/login/', UserLogin.as_view()),
    path('users/followers/<int:pk>/', UserFollowed.as_view()),
    path('users/following/<int:pk>/', UserFollow.as_view()),
    path('users/followingmoments/<int:pk>/', UserFollowingMoments.as_view()),
    path('users/changepass/<int:pk>/', UserChangePassword.as_view()),
    path('users/changedata/<int:pk>/', UserChangeNameandEmail.as_view()),
    path('users/changeprofilephoto/<int:pk>/', UserChangeProfilePhoto.as_view()),

    path('moments/', MomentView.as_view()),
    path('moments/create/', MomentCreate.as_view()),
    path('moments/edit/<int:pk>/', MomentEdit.as_view()),
    path('moments/delete/<int:pk>/', MomentDelete.as_view()),
    path('moments/<int:moment_id>/<int:user_id>/', MomentDetail.as_view()),
    path('moments/byuser/<int:pk>/', MomentByUser.as_view()),
    path('moments/statistic/<int:pk>/<int:user_id>/', MomentStatistic.as_view()),
    path('moments/popular/', cache_page(60 * 15)(MomentPopular.as_view())),

    path('comments/', CommentView.as_view()),
    path('comments/create/', CommentCreate.as_view()),
    path('comments/edit/<int:pk>/', CommentEdit.as_view()),
    path('comments/delete/<int:pk>/', CommentDelete.as_view()),
    path('comments/<int:pk>/', CommentDetail.as_view()),

    path('likes/', LikeView.as_view()),
    path('likes/create/', LikeCreate.as_view()),
    path('likes/edit/<int:pk>/', LikeEdit.as_view()),
    path('likes/delete/<int:pk>/', LikeDelete.as_view()),
    # path('likes/<int:pk>/', LikeDetail.as_view()),
    path('like/delete/moment/<int:id_author>/<int:id_moment>/', LikeDelete.as_view(), name='like-delete-moment'),
    path('like/delete/comment/<int:id_author>/<int:id_comment>/', LikeDelete.as_view(), name='like-delete-comment'),

    path('follows/', FollowView.as_view()),
    path('follows/create/', FollowCreate.as_view()),
    path('follows/edit/<int:pk>/', FollowEdit.as_view()),
    path('follows/delete/<int:id_follower>/<int:id_following>/', FollowDelete.as_view()),
    path('follows/<int:pk>/', FollowDetail.as_view()),

    path('tags/', TagView.as_view()),
    path('tags/create/', TagCreate.as_view()),
    path('tags/edit/<int:pk>/', TagEdit.as_view()),
    path('tags/delete/<int:pk>/', TagDelete.as_view()),
    path('tags/<int:pk>/', TagDetail.as_view()),
    path('tags/moment/<int:pk>/', TagByMoment.as_view()),
    
    path('search/', Search.as_view()),
]