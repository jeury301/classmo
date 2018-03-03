"""posts.py - Views for top-level posts (parentless comments)"""
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from discussions.forms import PostForm
from discussions.models import Post
from schedules.models import Subject

def index(request):
    """List all subjects and and link to corresponding
    discussion forums
    """
    subjects = Subject.objects.all().order_by('name')
    context = {'subjects': subjects}
    return render(request, 'discussions/posts/index.html', context)

def list_posts(request, subject_id):
    """List all posts in a given subject forum"""
    subj = get_object_or_404(Subject, id=subject_id)
    posts = Post.objects.filter(subject=subj).order_by('-created_date')
    context = {
        'posts': posts,
        'subject': subj
    }
    return render(request, 'discussions/posts/list.html', context)

def new_post(request, subject_id):
    subj = get_object_or_404(Subject, id=subject_id)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            post = Post.create(subject=subj,
                               title=title,
                               body=body,
                               author=request.user)
            post.save()
            return HttpResponseRedirect(reverse('list_posts', args=[subject_id]))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PostForm()

    context = {
        'form': form,
        'subject': subj
    }
    return render(request, 'discussions/posts/new_post.html', context)