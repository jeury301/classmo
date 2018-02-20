from django.urls import path
from .views import subjects, users, sessions
#from . import views

app_name='schedules'

urlpatterns = [
    path('', users.index, name='index'),
    path('register/',users.register,name='register'),
<<<<<<< HEAD
    #path('new_user/',users.new_user,name='new_user'),
    path('subjects/',subjects.subjects,name='subjects'),
    path('sessions/<int:session_id>/',sessions.sessions,name='sessions'),
   	path('sessions/<int:session_id>/registration',sessions.registration,name='registration'),
=======
    
    path('subjects/<int:subject_id>/detail',subjects.detail, name='detail'),
    path('subjects/<int:subject_id>/sessions',subjects.sessions, name='sessions'),
    path('sessions/<int:session_id>/detail',subjects.session, name='session'),
>>>>>>> 22d317153d275abf2eaf5a8ca8e47040e4cc5744
]