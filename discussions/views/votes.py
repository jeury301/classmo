"""posts.py - Views handling ajax calls related to votes"""
import json
import logging

from django.http import (Http404, HttpResponse, JsonResponse, 
                         HttpResponseBadRequest)
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect, csrf_exempt


from discussions.models import Vote, Comment, Post


@csrf_exempt
def cast_vote(request):
    logging.info(json.dumps(request.POST))
    if request.POST.get('type') == 'comment':
        comment_id = int(request.POST.get('commentId'))
        comment = get_object_or_404(Comment, id=comment_id)
        vote_value = int(request.POST.get('val'))
        old_score = comment.score
        new_vote = Vote.create(voter=request.user,
                               value=vote_value,
                               comment=comment)
        comment.refresh_from_db()
        response = {
            'new_score': comment.score,
            'old_score': old_score,
            'vote_value': vote_value,
            'vote_id': new_vote.id
        }
    elif request.POST.get('type') == 'post':
        post_id = int(request.POST.get('postId'))
        post = get_object_or_404(Post, id=post_id)
        vote_value = int(request.POST.get('val'))
        old_score = post.score
        new_vote = Vote.create(voter=request.user,
                               value=vote_value,
                               post=Post)
        post.refresh_from_db()
        response = {
            'new_score': post.score,
            'old_score': old_score,
            'vote_value': vote_value,
            'vote_id': new_vote.id
        }
    else:
        return HttpResponseBadRequest()
    return JsonResponse(response)

