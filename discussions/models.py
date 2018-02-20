import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from schedules.models import BaseModel, Subject

class Comment(BaseModel):
    """A model for discussion comments

    A top-level comment (a/k/a a post) will have itself for
    its post field and a null parent field

    A lower-level comment will have a top-level comment (post) for
    its post field and the comment to which it is responding as
    its parent field

    Fields:
        subject: The subject (e.g. Math 101) that top-level comments
            (or "posts") are organized under
        post: The top-level comment (or "post") in a thread
        parent: The comment or post to which the given post is
            replying.  For a top-level comment/post, this field
            is None
        author: The user who created the comment
        active: Whether the comment is active or not
        body: The body text of the comment
        score: The raw differential between upvotes and downvotes
        adjusted_score: The adjusted vote score
    """
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    post = models.ForeignKey('self', related_name='top_level_post',
                             on_delete=models.CASCADE, blank=True, null=True)
    parent = models.ForeignKey('self', related_name='parent_comment',
                               on_delete=models.CASCADE, blank=True, null=True)
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

    @classmethod
    def create_post(cls, **kwargs):
        """Create, save, and return a top-level comment (a/k/a post)

        This method sets the value of the post attribute to the
        newly-instantiated Comment itself

        The parent attribute is left blank for a top-level comment

        Kwargs:
            subject (obj): An instance of the Subject model representing
                the subject the post is associated withs
            body (string): The body text of the post

        Raises:
            TypeError if an invalid kwarg is passed, or if a required
                kwarg (body, subject) is missing
        """
        expected_keys = set(['subject', 'body'])
        if expected_keys != set(kwargs.keys()):
            raise TypeError("%s are required kwargs" % repr(expected_keys))
        post = Comment(subject=kwargs['subject'], body=kwargs['body'])
        post.save()
        post.post = post
        post.save()
        return post

    @classmethod
    def create_comment(cls, **kwargs):
        """Create, save, and return a lower-level comment

        Kwargs:
            body (string): The body text of the comment
            parent (obj): An instance of the Comment model representing
                the new comment's immediate parent in the thread

        Raises:
            TypeError if an invalid kwarg is passed, or if a required
                kwarg (body, subject) is missing
        """
        expected_keys = set(['body', 'parent'])
        if expected_keys != set(kwargs.keys()):
            raise TypeError("%s are required kwargs" % repr(expected_keys))
        comment = Comment(body=kwargs['body'], parent=kwargs['parent'])
        # Subject and post fields match the parent comment
        comment.subject = kwargs['parent'].subject
        comment.post = kwargs['parent'].post
        comment.save()
        return comment

    #TODO (@Michael): Write method for getting top-level posts
    # for a given subject



    #TODO (@Michael): Wite method for getting all comments for a given
    # top level post
