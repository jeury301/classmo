from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from operator import itemgetter 
from collections import OrderedDict

# Base model for others to inherit from
class BaseModel(models.Model):
    """Base model exists for the sole purpose of creating the created_date
    & modified_date with the correct date format
    """
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
    """Subject its a dump table that contains the list of subjects that the 
    system supports
    """
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.name

    @classmethod
    def fetch_all(cls):
        """Fetches list of objects
        """
        final_fetch = []
        for d_object in cls.objects.all():
            final_fetch.append(d_object)
        return final_fetch


class Location(BaseModel):
    """Location contains information about the location of a session.
    """
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

    @classmethod
    def fetch_all(cls):
        """Fetches list of objects
        """
        final_fetch = []
        for d_object in cls.objects.all():
            final_fetch.append(d_object)
        return final_fetch

class Session(BaseModel):
    """Session is the main entity for the scheduling app, which creates a rela-
    tionship between a subject, a location and a student.
    """
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    max_capacity = models.IntegerField(default=0)
    registered_students = models.IntegerField(default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

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
    def fetch_all(cls):
        """Fetches list of objects
        """
        final_fetch = []
        for d_object in cls.objects.all():
            final_fetch.append(d_object)
        return final_fetch

    @classmethod
    def order_by_upcoming(self,list):
        today=(datetime.now().weekday())-1
        today_time=datetime.now()
        h=(today_time.hour+today_time.minute/60)/24
        today+=h
        print("hours converted to days ",h)
        print("todays day= ",today)
        ordered_sessions=[]
        times_list={}
        for session in list:
            day=(session.start_date.weekday())-1
            day_hour=(session.start_date.hour+session.start_date.minute/60)/24
            day+=day_hour
            order=(day-today)
            if order < 0: 
                order+=6 
            ## this is the number of days between today and the session
            
            order+=day_hour
            times_list[order]=session
        times_list=OrderedDict(sorted(times_list.items(),key=itemgetter(0)))
        print(times_list)

        for key, value in times_list.items():
            ordered_sessions.append(value)
        return ordered_sessions


                

    @classmethod    
    def instructor_assignments(self,instructor):
        """Returns list of sessions assigned to current instructor
        """
        return self.objects.filter(instructor=instructor.pk)

    @classmethod
    def other_sessions(self, subject_id, student_id):
        """Returns old sessions for a given subject in which the current 
        student does not belong to
        """
        subject_sessions = self.objects.filter(subject=subject_id)
        final_sessions = []

        # filtering out sessions based off student's registrations
        for session in subject_sessions:
            print("Printing session: ")
            print(session)
            print("Checking other sessions")
            try:
                print("Checking count sessions")
                print(Registration.student_registration_for_session(student_id, 
                    session.id))
                if Registration.student_registration_for_session(student_id, 
                    session.id):
                    # student is registered for session, ignored.
                    pass
            except:
                # studesnt is not registered, lets add it
                final_sessions.append(session)
        return final_sessions

    @classmethod
    def my_sessions(self, subject_id, student_id):
        """Return current sessions for subject in which a student has been 
        registered
        """
        subject_sessions = self.objects.filter(subject=subject_id)
        final_sessions = []

        for session in subject_sessions:
            print("Checking my sessions")
            try:
                if Registration.student_registration_for_session(student_id, 
                    session.id):
                    # student is registered for session
                    final_sessions.append(session)
            except:
                pass
        return final_sessions

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
    def fetch_all(cls):
        """Fetches list of objects
        """
        final_fetch = []
        for d_object in cls.objects.all():
            final_fetch.append(d_object)
        return final_fetch

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

    @classmethod
    def session_students(cls, session_id):
        """Returns a list of students for a given session
        """
        return cls.objects.filter(session=session_id)

    @classmethod
    def subjects_for_student(cls, student_id):
        """Returns all subjects for a given student
        """
        registrations = cls.objects.filter(user=student_id)
        subjects = []

        for registration in registrations:
            # for registration check if subject is in list
            if registration.session.subject not in subjects:
                # new subject
                subjects.append(registration.session.subject) 
        return subjects


class Homework(BaseModel):
    """Homework contains data about homework assignments
    """
    name=models.CharField(max_length=200)
    #instructor=models.ForeignKey(User,on_delete=models.CASCADE)
    session=models.ForeignKey(Session,on_delete=models.CASCADE,
        default=1,null=True)
    description=models.CharField(max_length=200)
    due_date=models.DateTimeField(auto_now=False)
    def __str__(self):
        return self.name


class Profile(models.Model):
    """Profile contains metadata from the user that are not essential, 
    but its useful to have
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address_1 = models.CharField(max_length=128, default="")
    address_2 = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=128, default="New York")
    state = models.CharField(max_length=128, default="NY")
    zip_code = models.CharField(max_length=128, default="00000")
    country = models.CharField(max_length=128, default="United States")
    phone = models.CharField(max_length=128)

    def __str__(self):
        return self.user.username


    @classmethod
    def update_profile(cls, user, **profile_data):
        """Updating the user's profile with the information passed from the form
        """
        user.first_name = profile_data.get("first_name")
        user.last_name = profile_data.get("last_name")
        user.profile.address_1 = profile_data.get("address_1")
        user.profile.address_2 = profile_data.get("address_2")
        user.profile.city = profile_data.get("city")
        user.profile.state = profile_data.get("state")
        user.profile.zip_code = profile_data.get("zip_code")
        user.profile.country = profile_data.get("country")
        user.profile.phone = profile_data.get("phone_number")
        user.save()
        return True

    @classmethod
    def update_account(cls, user, **account_data):
        """Updating the user account with the information passed from the form
        """
        user.username = account_data.get("username")
        user.email = account_data.get("email")
        user.save()
        return True

    @classmethod
    def fetch_all(cls):
        """Fetches list of objects
        """
        final_fetch = []
        for d_object in cls.objects.all():
            final_fetch.append(d_object)
        return final_fetch
        




