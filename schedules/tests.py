from django.test import TestCase
from .models import Location, Subject, Session, Registration
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class SessionModelTests(TestCase):

    def test_user_already_registered_for_this_session(self):
    	time = timezone.now() + datetime.timedelta(days=30)
    	test_user=User.objects.create_user("Joe","poop@aol.com","fook")
    	test_user2=User.objects.create_user("Joe2","poop22@aol.com","fook22")
    	test_instructor=User.objects.create_user('Steve','poopy2@aol.com',"fook2")
    	test_subject=Subject(pk=1,name='Math',description="Math sucks")
    	test_location=Location(pk=1,name="New Jersey")
    	test_session=Session(pk=1,subject=test_subject,location=test_location,instructor=test_instructor,name="test sesh")
    	test_registration=Registration(pk=1,session=test_session,user=test_user)
    	test_user.save()
    	test_instructor.save()
    	test_subject.save()
    	test_location.save()
    	test_session.save()
    	test_registration.save()
    	check=test_session.is_registered(test_user) #this user is registered
    	self.assertTrue(check)
    	check=test_session.is_registered(test_user2) #this user should not be
    	self.assertFalse(check)
     

# Create your tests here.
