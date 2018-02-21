from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Base model for others to inherit from
class BaseModel(models.Model):
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.id:
            self.created_date = timezone.now()
        self.modified_date = timezone.now()
        return super(BaseModel, self).save(*args, **kwargs)


class Subject(BaseModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Location(BaseModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Session(BaseModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)


class Registration(BaseModel):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)