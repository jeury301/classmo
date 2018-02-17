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
    
    def __str__(self):
        return self.body
