from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from schedules.models import Subject, Location, Session, Profile
from discussions.models import Post, Comment, Vote

print("Cleaning up db.")

# cleaning up user data
User.objects.all().delete()
# cleaning up group data
Group.objects.all().delete()
# cleaning up subject, location, session, profile data
Subject.objects.all().delete()
Location.objects.all().delete()
Profile.objects.all().delete()
Session.objects.all().delete()
# cleaning up post, comment, vote data
Post.objects.all().delete()
Comment.objects.all().delete()
Vote.objects.all().delete()

exit()
