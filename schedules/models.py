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
    description = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.name


class Location(BaseModel):
    name = models.CharField(max_length=200)
    #TODO (@Jeury): add max capacity field and logic

    def __str__(self):
        return self.name

class Session(BaseModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    #TODO (@Jeury): add max capacity field

    #TODO (@Jeury): add create method with validation logic
    # - Is session max capacity more than location capacity
    # - Is session start date/end date in conflict with another session at
    # sane time and location

    def __str__(self):
        return self.name

    def is_registered(self,user):
        check=self.registration_set.filter(user=user).exists()
        return check

    def is_instructor(self,user):
        if self.instructor.pk==user.pk:
            return True
        else:
            return False

class Registration(BaseModel):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Assignment(BaseModel):
    name=models.CharField(max_length=200)
    #instructor=models.ForeignKey(User,on_delete=models.CASCADE)
    session=models.ForeignKey(Session,on_delete=models.CASCADE,default=1,null=True)
    description=models.CharField(max_length=200)
    due_date=models.DateTimeField(auto_now=False)
    def __str__(self):
        return self.name


