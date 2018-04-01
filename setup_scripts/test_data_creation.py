from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.utils import timezone
from django.conf import settings

from schedules.models import Subject, Location, Session, Profile
from setup_scripts.test_data import data
from setup_scripts.create_disc_demo import create_demo

from datetime import datetime, timedelta

def create_subjects(data, Subject):
    """Loading an initial set of subjects to the database
    """
    print("Loading subject data to db")
    # retrieving subjects from data
    subjects = data['subjects']['cs']

    # for each subject data, create a subject entity in db
    for subject in subjects:
        try:
            # avoiding duplicate subjects
            subject_check = Subject.objects.get(name=subject['name'])
        except Subject.DoesNotExist:
            # subject with name does not exists, let's create it
            subject_entity = Subject(
                name = subject['name'],
                description = subject['description']
            )
            subject_entity.save()
    print("Subject data loaded to db")

def create_locations(data, Location):
    """Loading an initial set of locations to the database
    """
    print("Loading location data to db")
    # retrieving locations from data
    locations = data['locations']

    # for each location data, create a location entity in db
    for location in locations:
        try:
            # avoiding duplicate locations
            location_check = Location.objects.get(name=location['name'])
        except Location.DoesNotExist:
            # location with name does not exists, let's create it
            location_entity = Location(
                name = location['name'],
                max_capacity = location['max_capacity'],
                address_1 = location['address_1'],
                city = location['city'],
                state = location['state'],
                zip_code = location['zip_code'],
                country = location['country']
            )
            location_entity.save()

    print("Location data loaded to db")

def create_instructors(data, settings, User, Group, Profile):
    """Loading an initial set of instructors to the database
    """
    print("Loading instructor data to db")
    # retrieving instructors from data
    instructors = data['instructors']

    # for each instructor data, create an instructor entity in db
    for instructor in instructors:
        try:
            # avoiding duplicate instructors/users
            user_check = User.objects.get(username=instructor['username'])
        except User.DoesNotExist:
            # instructor with username does not exists, let's create it
            username = instructor['username']
            email = instructor['email']
            password = instructor['password']

            # creating a user entity with instructor data
            instructor_entity = User.objects.create_user(
                username,email,password)

            instructor_entity.first_name = instructor['profile']['first_name']
            instructor_entity.last_name = instructor['profile']['last_name']
            instructor_entity.save()

            # adding instructor to instructor group
            instructor_group = Group.objects.get(name=settings.GROUPS["INSTRUCTORS"]) 
            instructor_group.user_set.add(instructor_entity)

    print("Instructor data loaded to db")

def create_sessions(data, settings, timezone, timedelta, Subject, Session, Location, User):
    """Creating sessions using current data in the database
    """
    from random import randint

    print("Loading session data to db")

    # retrieving sessions from data
    sessions = data['sessions']
    # retrieving all subjects
    subjects = Subject.fetch_all()
    # retrieving all locations
    locations = Location.fetch_all()

    # for each subject
    for subject in subjects:
        # for each session
        for index in range(0, len(sessions)):
            try:
                # avoiding duplicate sessions for subject
                session_check = Session.objects.get(subject=subject, name=sessions[index]['name'])
            except Session.DoesNotExist:
                # session with name for subject doesn't exist, lets create it
                session_entity = Session(
                    subject = subject,
                    location = locations[index],
                    instructor = User.objects.get(username=sessions[index]['instructor']),
                    name = sessions[index]['name'],
                    max_capacity = locations[index].max_capacity,
                    start_date = timezone.now(),
                    end_date = timezone.now() + timedelta(hours=randint(1, 4))
                )
                session_entity.save()

    print("Session data loaded to db")

def create_forums(settings, create_demo, Subject, User):
    """Creatin discussion data
    """
    print("Loading forum data to db")
    # retrieving all subjects
    subjects = Subject.fetch_all()
    # retrieving all instructor
    instructors = User.objects.filter(groups__name=settings.GROUPS["INSTRUCTORS"])
    instructors = [ins for ins in instructors]
    # calling Mike's super long function
    create_demo(subjects, instructors)

    print("Forum data loaded to db")

# initializing subject data
create_subjects(data, Subject)
# initializing location data
create_locations(data, Location)
# initializing instructor data
create_instructors(data, settings, User, Group, Profile)
# initializing session data
create_sessions(data, settings, timezone, timedelta, Subject,Session,Location, User)
# initializing forum data
create_forums(settings, create_demo, Subject, User)

exit()