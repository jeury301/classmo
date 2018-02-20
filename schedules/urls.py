from django.urls import path
from .views import subjects, users
#from . import views

app_name='schedules'

urlpatterns = [
    path('', users.index, name='index'),
    path('register/',users.register,name='register'),
    path('subjects/',subjects.subjects,name='subjects'),
    path('subjects/<int:subject_id>/detail',subjects.detail, name='detail'),
    path('subjects/<int:subject_id>/sessions',subjects.sessions, name='sessions'),
    path('sessions/<int:session_id>/detail',subjects.session, name='session'),
]