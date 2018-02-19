import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Comment
from schedules.models import BaseModel, Subject


class CommentModelTests(TestCase):

    def create_subject(self):
        """Creates, saves, and returns a subject object
        """
        subj = Subject(name="Algebra I")
        subj.save()
        return subj

    def create_a_post(self):
        """Creates and returns a post
        """
        subj = self.create_subject()
        post = Comment.create_post(subject=subj, body="I'm a top-level post")
        return post

    def test_post_parent_is_none(self):
        """When creating a top-level comment (a post), the value
        of the parent field should be None
        """
        subj = self.create_subject()
        post = Comment.create_post(subject=subj, body="I'm a top-level post")
        self.assertIs(post.parent, None)

    def test_post_post_is_self(self):
        """A top-level comment should have itself as the value
        of the post field
        """
        subj = self.create_subject()
        post = Comment.create_post(subject=subj, body="I'm a top-level post")
        self.assertIs(post.post, post)

    def test_create_post_bad_kwargs_raises_type_error(self):
        """Passing kwargs other than subject and body should raise
        TypeError
        """
        subj = self.create_subject()
        with self.assertRaises(TypeError):
            Comment.create_post(subject=subj, body="Hi", wrong="Oh no")

    def test_create_post_missing_kwarg_raises_type_error(self):
        """Not passing a required kwarg like body should raise type error
        """
        subj = self.create_subject()
        with self.assertRaises(TypeError):
            Comment.create_post(subject=subj)

    def test_create_comment_subject_not_none_when_parent_is_post(self):
        """A comment's subject field should not be None when its
        parent is a top-level post
        """
        post = self.create_a_post()
        comment = Comment.create_comment(body="I'm a comment", parent=post)
        self.assertIsNot(comment.subject, None)

    def test_create_comment_subject_matches_parent_when_parent_is_post(self):
        """A comment's subject field should match its parent when
        its parent is a post
        """
        post = self.create_a_post()
        comment = Comment.create_comment(body="I'm a comment", parent=post)
        self.assertIs(comment.subject, post.subject)

    def test_create_comment_subject_not_none_when_parent_is_comment(self):
        """A comment's subject feld should not be None when its parent
        is NOT a top-level post
        """
        post = self.create_a_post()
        parent = Comment.create_comment(body="I'm a parent comment", parent=post)
        comment = Comment.create_comment(body="I'm a child comment", parent=parent)
        self.assertIsNot(comment.subject, None)

    def test_create_comment_subject_matches_parent_when_parent_is_comment(self):
        """A comment's suject should match its parent when a parent
        is a child comment
        """
        post = self.create_a_post()
        parent = Comment.create_comment(body="I'm a parent comment", parent=post)
        comment = Comment.create_comment(body="I'm a child comment", parent=parent)
        self.assertIs(comment.subject, parent.subject)

    def test_create_comment_subject_matches_post_when_parent_not_post(self):
        """A comment's subject field should match that of the top-level
        post even whent the comment's parent is not itself a top-level
        post
        """
        post = self.create_a_post()
        parent = Comment.create_comment(body="I'm a parent comment", parent=post)
        comment = Comment.create_comment(body="I'm a child comment", parent=parent)
        self.assertIs(comment.subject, post.subject)


