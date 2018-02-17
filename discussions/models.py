from django.db import models
from schedules.models import BaseModel, Subject 

# Create your models here.
class Comment(BaseModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    post = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    active = models.BooleanField(default=True)
    body = models.TextField(max_length=3000)
    score = models.IntegerField(default=1)
    


