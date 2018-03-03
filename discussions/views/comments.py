"""comments.py - Views for child comments"""
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from discussions.forms import CommentForm
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


def new_top_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CommentForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data['body']
            comm = Comment.create(post=post,
                               body=body,
                               author=request.user)
            comm.save()
            return HttpResponseRedirect(
                reverse('list_comments', args=[comm.post.id]))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CommentForm()

    context = {
        'form': form,
        'post': post
    }
    return render(request, 'discussions/comments/new_top_comment.html', context)

def new_child_comment(request, comment_id):
    parent = get_object_or_404(Comment, id=comment_id)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CommentForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data['body']
            comm = Comment.create(parent=parent,
                               body=body,
                               author=request.user)
            comm.save()
            return HttpResponseRedirect(
                reverse('list_comments', args=[comm.post.id]))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CommentForm()

    context = {
        'form': form,
        'parent': parent
    }
    return render(request, 'discussions/comments/new_child_comment.html', context)