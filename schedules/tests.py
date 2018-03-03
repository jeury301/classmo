from django.test import TestCase
from .models import Location, Subject, Session, Registration
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

def create_shit():
    time = timezone.now() + datetime.timedelta(days=30)
    test_user=User.objects.create_user("Joe","poop@aol.com","fook")
    test_user2=User.objects.create_user("Joe2","poop22@aol.com","fook22")
    test_instructor=User.objects.create_user('Steve','poopy2@aol.com',"fook2")
    test_subject=Subject(pk=1,name='Math',description="Math sucks")
    test_location=Location(pk=1,name="New Jersey")
    test_session=Session(pk=1,subject=test_subject,location=test_location,instructor=test_instructor,name="test sesh")
    test_registration=Registration(pk=1,session=test_session,user=test_user)
    test_assignment=Assignment(pk=1,session=test_session,name="Test HW",description="A test HW",
        due_date=timezone.now()+datetime.timedelta(days=7))
    return {'test_user':test_user,'test_user2':test_user2,'test_instructor':test_instructor,
    'test_subject':test_subject,'test_location':test_location,'test_registration':test_registration,
    'test_session':test_session}

def create_shit_alt():
    time = timezone.now() + datetime.timedelta(days=30)
    test_user=User.objects.create_user("Joe5","poop@aol.com","fook")
    test_user2=User.objects.create_user("Joe6","poop22@aol.com","fook22")
    test_instructor=User.objects.create_user('SteveO','poopy2@aol.com',"fook2")
    test_subject=Subject(name='Math',description="Math sucks")
    test_subject.save()
    test_location=Location(name="New Jersey")
    test_location.save()
    test_session=Session(subject=test_subject,location=test_location,instructor=test_instructor,name="test sesh")
    test_session.save()
    test_registration=Registration(session=test_session,user=test_user)
    test_registration.save()
    return "OK"

def save(test_list):
    for var in test_list.values():
        var.save()
    
class SessionModelTests(TestCase):

    def test_user_already_registered_for_this_session(self):
        test_list=create_shit()
        save(test_list)
        check=test_list['test_session'].is_registered(test_list['test_user']) #this user is registered
        self.assertTrue(check)
        check=test_list['test_session'].is_registered(test_list['test_user2']) #this user should not be
        self.assertFalse(check)

    def test_user_is_instructor(self):
        test_list=create_shit()
        save(test_list)
        check=test_list['test_session'].is_instructor(test_list['test_instructor']) #this user is the instructor
        self.assertTrue(check)
        check=test_list['test_session'].is_instructor(test_list['test_user']) #this user is not an instuctor for this session
        self.assertFalse(check)

#class AssignmentModelTests(TestCase):




# Create your tests here.
