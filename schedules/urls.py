from django.urls import path
from .views import subjects, users, sessions
#from . import views

app_name='schedules'

urlpatterns = [
    # Home
    path('', users.index, name='index'),
    # My Sessions (instructors only)
    path('sessions/<request_type>',sessions.assignments,name='assignments'),
    # Session Students (instructors only)
    path('sessions/<int:session_id>/students', sessions.session_students, name='session_setudents'),
    # Drop Students (instructors only)
    path('sessions/drop_student/<int:registration_id>', sessions.drop_student, name='drop_student'),
    # Subjects (students only)
    path('subjects/<request_type>',subjects.subjects,name='subjects'),
    # Subject Sessions (students only)
    path('subjects/<int:subject_id>/sessions/<request_type>',subjects.sessions, name='sessions'),
    # Session Drop (students only)
    path('sessions/<int:session_id>/drop_session', sessions.drop_session, name='drop_session'),
    # Session Registration (students only)
    path('sessions/<int:session_id>/registration',sessions.registration,name='registration'),
    # Homeworks (students only)
    path('sessions/my_assignments',sessions.homework,name='homework'),
    # Session Details (all users)
    path('sessions/<int:session_id>/details',subjects.session, name='session'),
    # User registration (all users)
    path('register/',users.user_registration,name='register'),
    # User profile (all users)
    path('profile/',users.user_profile,name='profile'),
    path('pass_change',users.pass_change,name='pass_change'),
    # User account (all users)
    path('account/',users.user_account,name='account'),
    path('subjects/<int:subject_id>/details',subjects.detail, name='detail'),
    path('sessions/my_registrations',sessions.registrations,name='registrations')
]