import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Comment, Post
from schedules.models import BaseModel, Subject


def create_x_posts(x, subject):
    """Creates, saves, and returns a list of x posts"""
    posts = []
    for counter, value in enumerate("abcdefghijklmnopqrstuvwxyz"):
        posts.append(Post.create(subject=subject, body=(value*10)))
        posts[counter].save()

def create_basic_comment_tree():
    from discussions.models import Post, Comment
    import pprint

    mypost = create_a_post()
    print("mypost id: {}".format(mypost.id))

    #Direct responses
    comm1 = Comment.create(post=mypost, body="I'm comm1. I'm the first direct response to a post")
    comm1.save()
    comm2 = Comment.create(post=mypost, body="I'm comm2. I'm the second direct response to a post")
    comm2.save()

    # Responses to comm1
    comm3 = Comment.create(parent=comm1, body="I'm comm3. I'm the first response to comm1")
    comm3.save()
    comm4 = Comment.create(parent=comm1, body="I'm comm4. I'm the second response to comm1")
    comm4.save()

    # Responses to comm2
    comm5 = Comment.create(parent=comm2, body="I'm comm5. I'm the first response to comm2")
    comm5.save()
    comm6 = Comment.create(parent=comm2, body="I'm comm6. I'm the second response to comm2")
    comm6.save()

    # Response to comm3
    comm7 = Comment.create(parent=comm3, body="I'm comm7. I'm the only response to comm3")
    comm7.save()

    # Response to comm4
    comm8 = Comment.create(parent=comm4, body="I'm comm8. I'm the only response to comm4")
    comm8.save()

    # Response to comm5
    comm9 = Comment.create(parent=comm5, body="I'm comm9. I'm the only response to comm5")
    comm9.save()

    # Response to comm6
    comm10 = Comment.create(parent=comm6, body="I'm comm10. I'm the only response to comm6")
    comm10.save()

    print("mypost id: {}".format(mypost.id))

    tupp = Comment.get_comment_tree_tuple(mypost, 4, 'created_date')
    pprint.pprint(tupp)

def create_comment_trees_for_post(depth, children, post):
    """Creates, saves, and returns a list of comments for a post

    Arguments:
        depth - the depth of the comment tree
        children - the number of child comments each node in the
            comment tree has
        post - the post under which the comments are made
    """
    # FIXME: THIS DOESN'T WORK
    comments = []
    last_level = [None]
    current_level = []
    alpha = "abcdefghijklmnopqrstuvwxyz"
    max_depth = depth
    while depth > 0:
        cur_depth = max_depth - depth
        for parent in last_level:
            for i in range(children):
                current_level.append(Comment.create(parent=parent,
                                                    post=post,
                                                    body=(alpha[i%26]*5) + 
                                                          "(Depth{})".format(
                                                            cur_depth)))
        for comment in current_level:
            comment.save()
        comments += current_level
        last_level = current_level
        current_level = []
        depth -= 1
    return comments

def create_subject(name="Basket Weaving"):
    """Creates, saves, and returns a subject object"""
    subj = Subject(name=name)
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
