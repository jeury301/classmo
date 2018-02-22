"""posts.py - Views for top-level posts (parentless comments)"""
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from discussions.models import Post
from schedules.models import Subject

def list_posts(request, subject_id):
    subj = get_object_or_404(Subject, id=subject_id)
    posts = Post.objects.filter(subject=subj).order_by('-created_date')
    return render(request, 'discussions/posts/list.html', {'posts': posts})