from django.urls import path
from .views import PostListView, PostDetailView,UserPostListView
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='posts-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('about/',views.about,name='posts-about'),
    path('user-posts/<str:username>/',UserPostListView.as_view(),name='my-posts'),
    path('add-comment/',views.createNewComment,name='add-comment'),
    path('post/<int:post_id>/delete/', views.deletePost, name='post-delete'),


]
