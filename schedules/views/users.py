from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from ..forms import UserRegistrationForm
import json

def index(request):
	"""
	if request.user.is_authenticated:
		user=request.user
		session_list=user.registration_set.all()
		return render(request,'schedules/users/index.html',{"registrations":session_list})
		"""
	return render(request,'schedules/users/index.html')
	

@login_required
def my_sessions(request):
    if request.user.is_authenticated:
        user=request.user
        session_list=user.registration_set.all()
        return render(request,'schedules/users/index.html',{"registrations":session_list})
    return render(request,'schedules/users/index.html')

def register(request):
    """Proccessing registration for a new user.
    """
    username=request.POST.get('user','')
    password=request.POST.get('password','')
    email=request.POST.get('email','')
    fname=request.POST.get('fname','')
    lname=request.POST.get('lname','')
    user=User.objects.create_user(username,email,password)
    user.first_name=fname
    user.last_name=lname
    user.save()
    check = authenticate(request, username=username, password=password)
    if check is not None:
        login(request,user)
        return redirect('schedules:index')
    else:
        return HttpResponse("Something bad happened")
        #Comment

def user_registration(request):
    """Proccessing registration for a new user.
    """
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserRegistrationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            # creating a user
            user=User.objects.create_user(username,email,password)
            # upating a user
            user.first_name=first_name
            user.last_name=last_name
            user.profile.phone=phone_number
            user.save()

            check = authenticate(request, username=username, password=password)
            #return HttpResponse(json.dumps(form.cleaned_data), content_type='application/json')

            # authenticating user
            if check is not None:
                login(request,user)
                # redirect to a new URL:
                return redirect('schedules:index')
            else:
                return HttpResponse("Something terrible happened")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserRegistrationForm()

    return render(request, 'schedules/users/index.html', {'form': form})