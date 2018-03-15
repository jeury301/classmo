"""comments.py - Views for child comments"""
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from discussions.forms import CommentForm
from discussions.models import Comment, Post, Vote
from schedules.models import Subject


def list_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    max_depth = 5
    comments = Comment.get_ordered_comments(post, max_depth, '-created_date')
    context = {
        'post': post,
        'comments': comments,
        'max_depth': max_depth - 1 # Compensate for first element having 0 depth
    }
    return render(request, 'discussions/comments/list.html', context)


def detail_comment(request, comment_id):
    return HttpResponse("Hello from detail_comment")


@login_required
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
            # An upvote should automatically be cast by a user for 
            # their own comment
            Vote.create(voter=request.user, value=1, comment=comm)
            return HttpResponseRedirect(
                reverse('discussions:list_comments', args=[comm.post.id]))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CommentForm()

    context = {
        'form': form,
        'post': post
    }
    return render(request, 'discussions/comments/new_top_comment.html', context)


@login_required
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
            # An upvote should automatically be cast by a user for 
            # their own comment
            Vote.create(voter=request.user, value=1, comment=comm)
            return HttpResponseRedirect(
                reverse('discussions:list_comments', args=[comm.post.id]))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CommentForm()

    context = {
        'form': form,
        'parent': parent
    }
    return render(request, 'discussions/comments/new_child_comment.html', context)