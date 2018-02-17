from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse

def index(request):
    ##user=request.user gets user object
    return render(request,'schedules/users/index.html')

def new_user(request):
    username=request.POST.get('user','')
    password=request.POST.get('password','')
    user=User.objects.create_user(username,'invadeyou67@email.com',password)
    user.first_name='Attila'
    user.last_name="The hun"
    user.save()
    return HttpResponseRedirect(reverse('schedules:index'))
