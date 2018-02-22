import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from schedules.models import BaseModel, Subject

class BaseComment(BaseModel):
    """A base model for Comments and Posts

    Fields:
        author: The user who created the comment
        active: Whether the comment is active or not
        body: The body text of the comment
        score: The raw differential between upvotes and downvotes
        adjusted_score: The score, weighted by an algorithm TBD
    """
    class Meta:
        abstract = True

    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               blank=True, null=True)
    active = models.BooleanField(default=True)
    body = models.TextField(max_length=3000, default="")
    score = models.IntegerField(default=1)
    adjusted_score = models.FloatField(default=1.0)

    def __str__(self):
        """Prettified toString with max length of 53 chars"""
        msg = (self.body[:50] + '...') if len(self.body) > 53 else self.body
        return msg


class Post(BaseComment):
    """A model for top-level discussion forum posts

    Fields:
        subject: The subject (e.g. Math 101) that top-level posts
            are organized under

    Inherited fields from BaseComment:
        author, activ, body, score, adjusted_score
    """
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    @classmethod
    def create(cls, **kwargs):
        """Create and return a top-level post

        Kwargs:
            subject (obj): An instance of the Subject model
            body (string): The body text of the post
            author (obj): An instance of the Django User model (optional)

        Raises:
            TypeError if an invalid kwarg is passed, or if a required
                kwarg (body, subject, author) is missing
        """
        expected_keys = ['subject', 'body']
        for key in expected_keys:
            if key not in set(kwargs.keys()):
                raise TypeError("%s are required kwargs" % repr(expected_keys))
        post = Post(**kwargs)
        return post


class Comment(BaseComment):
    """A model for comments made in response to either a top-level
    post or another comment

    Fields:
        post: The top-level post in a thread
        parent: The comment to which the given post is replying.
            For a comment made directly in response to a top-level
            post, this field is None

    Inherited fields from BaseComment:
        author, activ, body, score, adjusted_score
    """
    post = models.ForeignKey(Post, related_name='top_level_post',
                             on_delete=models.CASCADE, blank=True, null=True)
    parent = models.ForeignKey('self', related_name='parent_comment',
                               on_delete=models.CASCADE, blank=True, null=True)
    @classmethod
    def create(cls, **kwargs):
        """Create, save, and return a comment

        Kwargs:
            body (string): The body text of the comment
            author (obj): An instance of the Django User model (optional)
            parent: An instance of the Comment model representing
                the new comment's immediate parent in the thread.
                Not required if comment is in response to a top-level
                post and 'post' is passed as kwarg
            post: The top-level post at the root of the discussion
                thread.  Not required if 'parent' is passed as kwarg

        Raises:
            TypeError if an invalid kwarg is passed, or if a required
                kwarg (body, subject) is missing
        """
        expected_keys = ['body']
        for key in expected_keys:
            if key not in set(kwargs.keys()):
                raise TypeError("%s are required kwargs" % repr(expected_keys))
        if kwargs.get('parent'):
            # If we have the a non-None parent, we can copy
            # the value of its 'post' attribute to its child
            # and disregard whatever 'post' kwarg was passed
            kwargs.pop('post', None)
            comment = Comment(**kwargs, post=kwargs.get('parent').post)
        elif kwargs.get('post'):
            # Otherwise, the 'post' field should have been
            # passed as a kwarg and the 'parent' field will
            # be set to None implicitly
            comment = Comment(**kwargs)
        else:
             raise TypeError("Either 'parent' or 'post' are required kwargs")
        return comment

