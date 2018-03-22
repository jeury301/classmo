from django.urls import path

from .views import comments, posts
app_name='discussions'

urlpatterns = [
    # path('', views.index, name='index'),
    path('', posts.index, name='discussion_index'),
    path('posts/<int:subject_id>/', posts.list_posts, name='list_posts'),
    path('comments/<int:post_id>/', comments.list_comments, 
         name='list_comments'),
    path('posts/<int:subject_id>/new/', posts.new_post, name='new_post'),
    path('comments/<int:post_id>/new_top/', comments.new_top_comment, 
         name='new_top'),
    path('comments/<int:comment_id>/new_child/', comments.new_child_comment, 
         name='new_child'),
]