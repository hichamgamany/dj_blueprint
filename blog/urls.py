from django.urls import path

from .views import (
    PostListView,
    PostFeaturedView,
    post_detail_view,
    CreatePostView,
    UpdatePostView,
    DeletePostView,
    UserPostView
)

urlpatterns = [
    path('articles/', PostListView.as_view(), name='post_list'),
    path('articles/featured/', PostFeaturedView.as_view(), name='posts_featured'),
    path('articles/user/', UserPostView.as_view(), name='user_post_list'),
    path('articles/create/', CreatePostView.as_view(), name='create_post'),
    path('articles/<str:slug>/', post_detail_view, name='post_detail'),
    path('articles/<str:slug>/update/', UpdatePostView.as_view(), name='update_post'),
    path('articles/<str:slug>/delete/', DeletePostView.as_view(), name='delete_post'),
]
