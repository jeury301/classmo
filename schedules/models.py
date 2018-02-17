from django.db import models

# Base model for others to inherit from
class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Create your models here.
class Subject(BaseModel):
    name = models.CharField(max_length=200)
