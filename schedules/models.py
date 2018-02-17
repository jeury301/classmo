from django.db import models
from django.contrib.auth.models import User

# Base model for others to inherit from
class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Subject(BaseModel):
    name = models.CharField(max_length=200)


class Location(BaseModel):
    name = models.CharField(max_length=200)


class Session(BaseModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)


class Registration(BaseModel):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)