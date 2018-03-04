from django.urls import path
from .views import subjects, users, sessions
#from . import views

app_name='schedules'

urlpatterns = [
    # Home
    path('', users.index, name='index'),
    # My Sessions (instructors only)
    path('sessions/my_sessions',sessions.assignments,name='assignments'),
    # Subjects (students only)
    path('subjects/',subjects.subjects,name='subjects'),
    # Homeworks (students only)
    path('sessions/my_assignments',sessions.homework,name='homework'),
    path('sessions/<int:session_id>/registration',sessions.registration,name='registration'),
    path('subjects/<int:subject_id>/detail',subjects.detail, name='detail'),
    path('subjects/<int:subject_id>/sessions',subjects.sessions, name='sessions'),
    path('sessions/<int:session_id>/detail',subjects.session, name='session'),
    path('sessions/my_registrations',sessions.registrations,name='registrations'),
    path('sessions/<int:session_id>/drop_session', sessions.drop_session, name='drop_session'),
    path('register/',users.user_registration,name='register'),

]