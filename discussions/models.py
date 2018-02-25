from django.contrib.auth.models import User
from django.db import models

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

    @classmethod
    def get_comment_tree_tuple(cls, post, max_depth, order_by):
        """Returns a tree-like nested tuple that models parent
        and child comments under a given post

        Returned tuple is of the form

            (comment_object, depth_of_comment, [list_of_other_tuples])
        """

        def get_children(parent, comment_list):
            """Given a list of comments, 'comment_list', returns a tuple
            of two lists:

            1.) a list containing children of the 'parent' contained
            in 'comment_list'
            2.) a list containing the elements in 'comment_list', except
            the children of the 'parent' comment
            """
            children = []
            other_comments = []
            for comment in comment_list:
                if parent is None:
                    if comment.parent is None:
                        children.append(comment)
                    else:
                        other_comments.append(comment)
                else:
                    if comment.parent == parent:
                        children.append(comment)
                    else:
                        other_comments.append(comment)
            return (children, other_comments)

        comment_list = list(Comment.objects.filter(post=post).order_by(order_by))
        depth = 0
        big_tuple = (None, None, [])

        if not comment_list:
            return big_tuple

        old_tuples = [big_tuple]
        new_tuples = []
        while depth < max_depth:
            for cur_tuple in old_tuples:
                cur_head = cur_tuple[0]
                cur_tail = cur_tuple[2]
                children, comment_list = get_children(cur_head, comment_list)
                for child in children:
                    child_tuple = (child, depth, [])
                    cur_tail.append(child_tuple)
                    new_tuples.append(child_tuple)
            old_tuples = new_tuples
            new_tuples = []
            depth += 1
        return big_tuple

    @classmethod
    def get_ordered_comments(cls, post, max_depth, order_by):
        """Return a list of dicts representing comments
        with metadata about absolute and relative depth
        of the comment in the comment tree

        Format of the dicts is as follows:

        {
            'comment': a_comment_object,
            'abs_depth': an_integer,
            'rel_depth': an_integer,
            'depth_counter': an_integer
        }

        abs_depth is how many ancestor comments
        the comment has (0  for a comment made directly
        in reply to a post)

        rel_depth is the difference between the absolute depth
        of the instant element in the and list the previous
        indent. This is used when determining the indentation
        level of a commment when rendering a template.

        depth_counter is a string that, insanely, is used as a loop
        counter by the Django template.  We should have used Jinja2.

        """
        tree = cls.get_comment_tree_tuple(post, max_depth, order_by)
        stack = []
        output = []
        # By doing a pre-order traversal of the comment tree,
        # we get the comments listed in the order they should
        # be displayed in the template
        stack.append(tree)
        while stack:
            parent = stack.pop()
            if parent[0]: #Ignore the first node with head set to None
                new_dict = {
                    'comment': parent[0],
                    'abs_depth': parent[1],
                    'rel_depth': None,
                    'depth_counter': None
                }
                output.append(new_dict)
            for child in parent[2]:  # Second element of tup is children list
                stack.append(child)

        # Now that we have a list of comments in order, we need
        # to complete the rel_depth and depth_counter fields in
        # each dict so we can either indent or unindent each
        # comment relative to the last comment in the list when
        # displaying them
        if output:
            parent_depth = output[0]['abs_depth']
            for comm_dict in output:
                comm_dict['rel_depth'] = comm_dict['abs_depth'] - parent_depth
                comm_dict['depth_counter'] = abs(comm_dict['rel_depth']) * "x"
                parent_depth = comm_dict['abs_depth']
        return output
