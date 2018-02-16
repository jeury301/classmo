from django.db import models

# Create your models here.
class Class(models.Model):
    class_name = models.CharField(max_length=200)
