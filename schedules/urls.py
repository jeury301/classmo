from django.urls import path
from .views import subjects, users, sessions
#from . import views

app_name='schedules'

urlpatterns = [
    path('', users.user_registration, name='index'),
    path('register/',users.user_registration,name='register'),
    #path('new_user/',users.new_user,name='new_user'),
    path('subjects/',subjects.subjects,name='subjects'),
    #redundant after merge with jeury's view
    #path('sessions/<int:session_id>/',sessions.sessions,name='sessions'),
    path('sessions/<int:session_id>/registration',sessions.registration,name='registration'),
    path('subjects/<int:subject_id>/detail',subjects.detail, name='detail'),
    path('subjects/<int:subject_id>/sessions',subjects.sessions, name='sessions'),
    path('sessions/<int:session_id>/detail',subjects.session, name='session'),
    path('sessions/my_assignments',sessions.homework,name='homework'),
    path('sessions/my_sessions',sessions.assignments,name='assignments'),
    path('sessions/my_registrations',sessions.registrations,name='registrations'),
    path('users/my_sessions',users.my_sessions,name='my_sessions'),
    path('sessions/<int:session_id>/drop_session', sessions.drop_session, name='drop_session')

]