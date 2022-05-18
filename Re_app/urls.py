from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,)

app_name = "Re_app"

urlpatterns = [
    path("api/authenticate",views.authenticate,name="Authentication"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/follow/<str:pk>/',views.follow,name='follow'),
    path('api/unfollow/<str:pk>/',views.unfollow,name='unfollow'),
    path('api/user',views.get_user,name="get_user"),
    path('api/posts',views.create_post,name="create_post"),
    path('api/posts/<str:pk>', views.delete_post,name="post_operation"),
    path('api/like/<str:pk>',views.like,name="like"),
    path('api/unlike/<str:pk>',views.unlike,name="unlike"),
    path('api/comment/<pk>',views.add_comment,name="add_comment"),
    path('api/all_posts',views.all_posts,name="all_posts")
]

