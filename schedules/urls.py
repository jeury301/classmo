from django.urls import path
from .views import subjects, users
#from . import views

app_name='schedules'

urlpatterns = [
    path('', users.index, name='index'),
    path('new_user/',users.new_user,name='new_user'),
    path('subjects/',subjects.subjects,name='subjects')
]