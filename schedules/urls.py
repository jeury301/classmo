from django.urls import path
from .views import subjects, users, sessions
#from . import views

app_name='schedules'

urlpatterns = [
    # Home
    path('', users.index, name='index'),
    # My Sessions (instructors only)
    path('sessions/<request_type>',sessions.assignments,name='assignments'),
    # Session Details
    path('sessions/<int:session_id>/details',subjects.session, name='session'),
    # Session Students (instructors only)
    path('sessions/<int:session_id>/students', sessions.session_students, name='session_setudents'),
    # Subjects (students only)
    path('subjects/<request_type>',subjects.subjects,name='subjects'),
    # Homeworks (students only)
    path('sessions/my_assignments',sessions.homework,name='homework'),
    # User registration
    path('register/',users.user_registration,name='register'),
    # User profile
    path('profile/',users.user_profile,name='profile'),
    # User account
    path('account/',users.user_account,name='account'),
    path('sessions/<int:session_id>/registration',sessions.registration,name='registration'),
    path('subjects/<int:subject_id>/details',subjects.detail, name='detail'),
    path('subjects/<int:subject_id>/sessions',subjects.sessions, name='sessions'),
    path('sessions/my_registrations',sessions.registrations,name='registrations'),
    path('sessions/<int:session_id>/drop_session', sessions.drop_session, name='drop_session'),
]