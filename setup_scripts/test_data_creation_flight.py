from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.utils import timezone
from django.conf import settings

from schedules.models import Subject, Location, Session, Profile, Config
from setup_scripts.test_data_flight import data
from setup_scripts.config_data import config_data
from setup_scripts.create_disc_demo import create_demo

from datetime import datetime, timedelta

def create_subjects(data, Subject):
    """Loading an initial set of subjects to the database
    """
    print("Loading subject data to db")
    # retrieving subjects from data
    subjects = data['subjects']['flight']

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
                start_date = timezone.now() + timedelta(days=randint(1,90))
                # session with name for subject doesn't exist, lets create it
                session_entity = Session(
                    subject = subject,
                    location = locations[index],
                    instructor = User.objects.get(username=sessions[index]['instructor']),
                    name = sessions[index]['name'],
                    max_capacity = locations[index].max_capacity,
                    start_date = start_date,
                    end_date = start_date + timedelta(hours=randint(1, 4))
                )
                session_entity.save()

    print("Session data loaded to db")

def create_configs(config_data, Config):
    """Loading an initial set of configs to the database
    """
    print("Loading config data to db")
    # retrieving subjects from data
    configs = config_data['configs']

    # for each config data, create a config entity in db
    for config in configs:
        try:
            # avoiding duplicate configs
            config_check = Config.objects.get(company=config['company'])
        except Config.DoesNotExist:
            # config with company name does not exists, let's create it

            is_active = False
            # activating flight configuration
            if config['name'] == "flight":
                is_active = True

            config_entity = Config(
                company = config['company'],
                primary_color = config['primary_color'],
                secondary_color = config['secondary_color'],
                logo = config['logo'],
                slogan = config['slogan'],
                font_family = config['font_family'],
                welcome_title = config['welcome_title'],
                welcome_body = config['welcome_body'],
                all_courses_body = config['all_courses_body'],
                my_courses_body = config['my_courses_body'],
                discussion_body = config['discussion_body'],
                primary_text_color = config['primary_text_color'],
                secondary_text_color = config['secondary_text_color'],
                jumbotron_color = config['jumbotron_color'],
                splash_url_1 = config['splash_url_1'],
                splash_url_2 = config['splash_url_2'],
                splash_url_3 = config['splash_url_3'],
                splash_license_1 = config['splash_license_1'],
                splash_license_2 = config['splash_license_2'],
                splash_license_3 = config['splash_license_3'],
                small_logo = config['small_logo'],
                is_active = is_active
            )
            config_entity.save()
    print("Config data loaded to db")

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
# initializing config data
create_configs(config_data, Config)
# initializing forum data
create_forums(settings, create_demo, Subject, User)

exit()
