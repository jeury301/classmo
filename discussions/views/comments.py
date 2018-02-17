"""posts.py - Views for child comments"""
from django.http import HttpResponse

from discussions.models import Comment

def list_comments(request, post_id):
    return HttpResponse("Hello from list_comments")

def detail_comment(request, comment_id):
    return HttpResponse("Hello from detail_comment")