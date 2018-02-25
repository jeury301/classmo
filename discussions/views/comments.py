"""posts.py - Views for child comments"""
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from discussions.models import Comment, Post
from schedules.models import Subject

def list_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.get_ordered_comments(post, 4, '-created_date')
    return render(request, 'discussions/comments/list.html',
        {'post': post,
         'comments': comments})

def detail_comment(request, comment_id):
    return HttpResponse("Hello from detail_comment")