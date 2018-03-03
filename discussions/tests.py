import datetime

from django.contrib.auth.models import User
from django.utils import timezone
from django.test import TestCase

from .models import Comment, Post, Vote
from schedules.models import BaseModel, Subject

DEFAULT_SCORE = 1 # Default score for comments and posts

def create_x_posts(x, subject):
    """Creates, saves, and returns a list of x posts"""
    posts = []
    for counter, value in enumerate("abcdefghijklmnopqrstuvwxyz"):
        posts.append(Post.create(subject=subject, title=(value*10), body=(value*100)))
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
    post = Post.create(subject=subj, title="A great title", body="Just a great day!")
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


class VoteModelTests(TestCase):

    def setUp(self):
        """We need a subject, post, comment, and user for our tests"""
        subj = create_subject()
        subj.save()
        post = Post.create(subject=subj, title="123ABC", body="123ABC Body")
        post.save()
        comment = Comment.create(post=post, body="987XYZ")
        comment.save()
        # Create and login user
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')

    # FIXME: These two tests really concern the Comment/Post models
    def test_default_score_post(self):
        """The value of a Post's score attribute after being
        instantiated should be equal to DEFAULT_SCORE"""
        post = Post.objects.get(body="123ABC Body")
        self.assertEqual(post.score, DEFAULT_SCORE)

    def test_default_score_comment(self):
        """The value of a Comment's score attribute after being
        instantiated should be equal to DEFAULT_SCORE"""
        comment = Comment.objects.get(body="987XYZ")
        self.assertEqual(comment.score, DEFAULT_SCORE)

    def test_vote_created_for_post(self):
        """Make sure Vote object gets instantiated correctly when  
        post is passed as kwarg
        """
        post = Post.objects.get(body="123ABC Body")
        vote = Vote.create(post=post, value=1, voter=self.user)
        vote.save()
        self.assertIsNotNone(vote)
        self.assertIsNotNone(vote.post)
        self.assertIsNotNone(vote.topic_post)
        self.assertIsNotNone(vote.voter)
        self.assertIs(vote.post, post)
        self.assertIs(vote.topic_post, post)
        self.assertIs(vote.voter, self.user)

    def test_vote_created_for_comment(self):
        """Make sure Vote object gets instantiated correctly when 
        comment is passed as kwarg
        """
        comment = Comment.objects.get(body="987XYZ")
        vote = Vote.create(comment=comment, value=1, voter=self.user)
        vote.save()
        self.assertIsNotNone(vote)
        self.assertIsNotNone(vote.comment)
        self.assertIsNotNone(vote.topic_post)
        self.assertIsNotNone(vote.voter)
        self.assertIs(vote.comment, comment)
        self.assertIs(vote.topic_post, comment.post)
        self.assertIs(vote.voter, self.user)

    def test_upvote_modifies_post_score(self):
        """A new Vote on a post being instantiated should
        increase the corresponding post's score attribute 
        by one
        """
        post = Post.objects.get(body="123ABC Body")
        self.assertEqual(post.score, DEFAULT_SCORE)
        vote = Vote.create(post=post, value=1, voter=self.user)
        post = Post.objects.get(body="123ABC Body")
        self.assertEqual(post.score, DEFAULT_SCORE + 1)

    def test_upvote_modifies_comment_score(self):
        """A new upvote on a comment being instantiated should
        increase the corresponding comment's score attribute 
        by one
        """
        comment = Comment.objects.get(body="987XYZ")
        self.assertEqual(comment.score, DEFAULT_SCORE)
        vote = Vote.create(comment=comment, value=1, voter=self.user)
        comment = Comment.objects.get(body="987XYZ")
        self.assertEqual(comment.score, DEFAULT_SCORE + 1)

    def test_downvote_modifies_post_score(self):
        post = Post.objects.get(body="123ABC Body")
        self.assertEqual(post.score, DEFAULT_SCORE)
        vote = Vote.create(post=post, value=-1, voter=self.user)
        post = Post.objects.get(body="123ABC Body")
        self.assertEqual(post.score, DEFAULT_SCORE - 1)

    def test_downvote_modifies_comment_score(self):
        """A new downvote on a comment being instantiated should
        decrease the corresponding comment's score attribute 
        by one
        """
        comment = Comment.objects.get(body="987XYZ")
        self.assertEqual(comment.score, DEFAULT_SCORE)
        vote = Vote.create(comment=comment, value=-1, voter=self.user)
        comment = Comment.objects.get(body="987XYZ")
        self.assertEqual(comment.score, DEFAULT_SCORE - 1)

    def test_upvote_then_downvote_same_user_leaves_post_score_one_less(self):
        """Creating an upvote, then a downvote, for the same
        user on a given post should leave the post's score
        as one less than its original value
        """
        post = Post.objects.get(body="123ABC Body")
        # self.assertEqual(len(post_qs), 1)
        self.assertEqual(post.score, DEFAULT_SCORE)
        post = Post.objects.get(body="123ABC Body")

        vote1 = Vote.create(post=post, value=1, voter=self.user)
        post = Post.objects.get(body="123ABC Body")
        self.assertEqual(post.score, DEFAULT_SCORE + 1)

        vote2 = Vote.create(post=post, value=-1, voter=self.user)
        post = Post.objects.get(body="123ABC Body")
        self.assertEqual(post.score, DEFAULT_SCORE - 1)

    def test_upvote_then_downvote_same_user_leaves_comment_score_one_less(self):
        """Creating an upvote, then a downvote, for the same
        user on a given comment should leave the comment's score
        as one less than its original value
        """
        comment = Comment.objects.get(body="987XYZ")
        # self.assertEqual(len(post_qs), 1)
        self.assertEqual(comment.score, DEFAULT_SCORE)
        comment = Comment.objects.get(body="987XYZ")

        vote1 = Vote.create(comment=comment, value=1, voter=self.user)
        comment = Comment.objects.get(body="987XYZ")
        self.assertEqual(comment.score, DEFAULT_SCORE + 1)

        vote2 = Vote.create(comment=comment, value=-1, voter=self.user)
        comment = Comment.objects.get(body="987XYZ")
        self.assertEqual(comment.score, DEFAULT_SCORE - 1)

    def test_downvote_then_upvote_same_user_leaves_post_score_one_greater(self):
        """Creating an upvote, then a downvote, for the same
        user on a given post should leave the post's score
        as one more than its original value
        """
        post = Post.objects.get(body="123ABC Body")
        # self.assertEqual(len(post_qs), 1)
        self.assertEqual(post.score, DEFAULT_SCORE)
        post = Post.objects.get(body="123ABC Body")

        vote1 = Vote.create(post=post, value=-1, voter=self.user)
        post = Post.objects.get(body="123ABC Body")
        self.assertEqual(post.score, DEFAULT_SCORE - 1)

        vote2 = Vote.create(post=post, value=1, voter=self.user)
        post = Post.objects.get(body="123ABC Body")
        self.assertEqual(post.score, DEFAULT_SCORE + 1)

    def test_downvote_then_upvote_same_user_leaves_comment_score_one_greater(self):
        """Creating a downvote, then an upvote, for the same
        user on a given comment should leave the comment's score
        as one less than its original value
        """
        comment = Comment.objects.get(body="987XYZ")
        # self.assertEqual(len(post_qs), 1)
        self.assertEqual(comment.score, DEFAULT_SCORE)
        comment = Comment.objects.get(body="987XYZ")

        vote1 = Vote.create(comment=comment, value=-1, voter=self.user)
        comment = Comment.objects.get(body="987XYZ")
        self.assertEqual(comment.score, DEFAULT_SCORE - 1)

        vote2 = Vote.create(comment=comment, value=1, voter=self.user)
        comment = Comment.objects.get(body="987XYZ")
        self.assertEqual(comment.score, DEFAULT_SCORE + 1)

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
