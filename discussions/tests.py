import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Comment, Post
from schedules.models import BaseModel, Subject


def create_subject():
    """Creates, saves, and returns a subject object"""
    subj = Subject(name="Algebra I")
    subj.save()
    return subj

def create_a_post():
    """Creates, saves, and returns a post"""
    subj = create_subject()
    post = Post.create(subject=subj, body="I'm a top-level post")
    post.save()
    return post

def create_comment_immediately_below_post():
    """Creates, saves, and returns a comment without a parent,
    i.e., a comment responding directly to a post
    """
    post = create_a_post()
    comment = Comment.create(post=post, body="I'm a comment right below a post")
    comment.save()
    return comment

def create_comment_with_parent_comment(self):
    parent = create_comment_immediately_below_post()
    comment = Comment.create(parent=parent, body="I'm a child comment")


class CommentModelTests(TestCase):

    def test_create_comment_missing_kwarg_raises_type_error(self):
        """Not passing a required kwarg like body should raise type error
        """
        post = create_a_post()
        with self.assertRaises(TypeError):
            comment = Comment.create(post=post)

    def test_create_comment_either_parent_or_post_must_be_kwarg(self):
        """If neither 'parent' nor 'post' are passed as kwarg keys,
        a TypeError should be raised
        """
        post = create_a_post()
        with self.assertRaises(TypeError):
            Comment.create(body="This shouldn't work")

    def test_create_comment_parent_is_none_when_post_is_kwarg(self):
        """A comment's 'parent' field should be none when 'post' is
        passed as a kwarg
        """
        post = create_a_post()
        comment = Comment.create(body="I'm a comment without a parent", post=post)
        self.assertIs(comment.parent, None)

    def test_post_matches_parent_when_parent_is_comment(self):
        """A comment's 'post'field should match its parent it when has a
        non-None parent
        """
        post = create_a_post()
        parent = Comment.create(body="I'm a parent comment", post=post)
        comment = Comment.create(body="I'm a child comment", parent=parent)
        self.assertIs(comment.post, parent.post)

    def test_post_is_not_none_when_parent_is_kwarg(self):
        """A comment's post field should not be none when parent
        is passed in as a a kwarg to create()
        """
        post = create_a_post()
        parent = Comment.create(body="I'm a parent comment", post=post)
        comment = Comment.create(body="I'm a child comment", parent=parent)
        self.assertIsNotNone(comment.post)

class PostModelTests(TestCase):

    def test_create_post_missing_kwarg_raises_type_error(self):
        """Not passing a required kwarg like body should raise type error
        """
        subj = create_subject()
        with self.assertRaises(TypeError):
            Post.create(subject=subj)