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
    max_capacity = models.IntegerField(default=0)
    address_1 = models.CharField(max_length=128, default="")
    address_2 = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=64, default="New York")
    state = models.CharField(max_length=2, default="NY")
    zip_code = models.CharField(max_length=5, default="00000")
    country = models.CharField(max_length=128, default="United States")

    def __str__(self):
        return self.name

class Session(BaseModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    max_capacity = models.IntegerField(default=0)
    registered_students = models.IntegerField(default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
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

    @classmethod    
    def instructor_assignments(self,instructor):
        """Returns list of sessions assigned to current instructor
        """
        return self.objects.filter(instructor=instructor.pk)

class Registration(BaseModel):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """On save, update session and validate this registration
        """
        if not self.registration_validator():
            # updating session registration count
            session = self.session
            session.registered_students += 1
            session.save()
            super(Registration, self).save(*args, **kwargs)
            return True
        else:
            return False

    def delete(self, *args, **kwargs):
        """On delete, update session
        """
        session = self.session
        current_registered = session.registered_students - 1

        if current_registered < 0:
            current_registered = 0
        session.registered_students=current_registered
        session.save()
        return super(Registration, self).delete(*args, **kwargs)

    def registration_validator(self):
        """Validating registration before creation. A registration will be 
        created, only if any of the following violations occur:
        - registered_students == max_capacity
        - some undefined ones yet
        """
        registered_students_count = self.session.registered_students
        max_capacity = self.session.max_capacity

        print("Registered Count: {}".format(registered_students_count))
        print("Max Capacity: {}".format(max_capacity))

        violations = []

        if registered_students_count >= max_capacity:
            # session is full
            violations.append(1)
        return bool(violations)
        
    @classmethod    
    def student_registrations(cls,student):
        """Returns list of registrations for given students
        """
        return cls.objects.filter(user=student.pk)

    @classmethod
    def student_registration_for_session(cls, student, session):
        """Returns the student's registration for a given session
        """
        return cls.objects.get(user=student, session=session)

class Homework(BaseModel):
    name=models.CharField(max_length=200)
    #instructor=models.ForeignKey(User,on_delete=models.CASCADE)
    session=models.ForeignKey(Session,on_delete=models.CASCADE,default=1,null=True)
    description=models.CharField(max_length=200)
    due_date=models.DateTimeField(auto_now=False)
    def __str__(self):
        return self.name


