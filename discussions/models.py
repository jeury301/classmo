from django.db import models
from schedules.models import BaseModel, Subject 

# Create your models here.
class Comment(BaseModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    post = models.ForeignKey('self', related_name='top_level_post', 
                             on_delete=models.CASCADE, blank=True, null=True)
    parent = models.ForeignKey('self', related_name='parent_comment',
                                on_delete=models.CASCADE, blank=True, null=True)
    active = models.BooleanField(default=True)
    body = models.TextField(max_length=3000, default="")
    score = models.IntegerField(default=1)
    
    # TODO (@Michaal): Prettify toString with truncation
    def __str__(self):
        msg = (self.body[:50] + '...') if len(self.body) > 53 else self.body
        return msg

    #TODO (@Michael): write method for creating top-level Comment
    @classmethod
    def create_post(self, **kwargs):
        expected_keys = set('subject', 'body')
        if expected_keys != set(kwargs.keys()):
            raise ValueError("Kwargs keys do not match expected keys")
        post = Comment(subject=subject, body=body)
        post.save()
        post.post = post.id
        post.save()
        return posts

    #TODO (@Michael): write method for creating child Comment
    # @classmethod
    # def create_comment(self, **kwargs):