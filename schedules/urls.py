from django.urls import path
from .views import subjects, users, sessions
#from . import views

app_name='schedules'

urlpatterns = [
    path('', users.index, name='index'),
    path('register/',users.register,name='register'),
    #path('new_user/',users.new_user,name='new_user'),
    path('subjects/',subjects.subjects,name='subjects'),
    path('sessions/<int:session_id>/',sessions.sessions,name='sessions'),
   	path('sessions/<int:session_id>/registration',sessions.registration,name='registration')
]