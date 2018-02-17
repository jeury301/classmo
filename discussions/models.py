from django.db import models
from schedules.models import Subject 

# Create your models here.
class Comment(models.Model):
    question_text = models.CharField(max_length=200)
    class_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
