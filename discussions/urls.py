from django.urls import path

from .views import comments, posts

urlpatterns = [
    # path('', views.index, name='index'),
    path('posts/<int:subject_id>/', posts.list_posts, name='list_posts'),
    path('comments/<int:post_id>/', comments.list_comments, 
         name='list_comments'),
]