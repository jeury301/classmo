"""posts.py - Views for top-level posts (parentless comments)"""
from django.http import HttpResponse

from discussions.models import Comment

def list_posts(request, subject_id):
    return HttpResponse("Hello from list_posts")