from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from schedules.services import portal_tools
from schedules.services.portal_tools import instructors_only, students_only
from schedules.models import Profile, Session
from discussions.models import Post, Comment
from datetime import date
from ..forms import UserRegistrationForm, UserProfileForm, UserAccountForm
import json
from django.conf import settings



def index(request):
    if request.user.is_authenticated:
        current_user=request.user
        post_list=[]
        sesh_list=[]
        is_instructor = portal_tools.is_member(current_user, settings.GROUPS["INSTRUCTORS"])
        is_student = portal_tools.is_member(current_user, settings.GROUPS["STUDENTS"])
        if is_student:
            session_list=current_user.registration_set.all()
            for sesh in session_list:
                sesh_list.append(sesh.session)
            temp=Session.order_by_upcoming(sesh_list)
            for reg in session_list:
                instructor=reg.session.instructor
                l=Post.objects.filter(author=instructor).filter(subject=reg.session.subject).order_by('-created_date')[:5] 
                post_list+=l
            return render(request,'schedules/users/index.html',{"registrations":session_list,"is_instructor":is_instructor,"is_student":is_student,"post_list":post_list})

        if is_instructor:
            temp=[]
            session_list=current_user.session_set.all()
            for sesh in session_list:
                sesh_list.append(sesh)
            temp=Session.order_by_upcoming(sesh_list)

            for reg in session_list:
                subject=reg.subject
                l=Post.objects.filter(subject=subject).exclude(author=current_user).order_by('-created_date')[:5]
                post_list+=l
            session_list=temp
            return render(request,'schedules/users/index.html',{"registrations":session_list,"is_instructor":is_instructor,"is_student":is_student,"post_list":post_list})
        else:
            return render(request,'schedules/users/index.html',{"is_instructor":is_instructor,"is_student":is_student,"post_list":post_list})
            
    else:
        return render(request,'schedules/users/splash.html')
	

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
            # creating a user
            user=User.objects.create_user(username,email,password)

            check = authenticate(request, username=username, password=password)
            #return HttpResponse(json.dumps(form.cleaned_data), content_type='application/json')

            # authenticating user
            if check is not None:
                login(request,user)
                messages.add_message(request, messages.SUCCESS, 
                '<strong>Congrats!</strong> your account '
                'have been successfully created.', 
                extra_tags='safe')

                # adding user to the student group
                student_group = Group.objects.get(name=settings.GROUPS["STUDENTS"]) 
                student_group.user_set.add(user)

                # redirect to a prfile
                return redirect('schedules:index')
            else:
                return HttpResponse("Something terrible happened")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserRegistrationForm()

    return render(request, 'schedules/users/register.html', {'form': form})

@login_required
def user_profile(request):
    """Processing user profile update.
    """
    current_user = User.objects.get(pk=request.user.pk)
    current_profile = Profile.objects.get(user=request.user)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserProfileForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required

            # updating the user's profile
            is_updated = Profile.update_profile(request.user, 
                **form.cleaned_data)
            if is_updated:
                messages.add_message(request, messages.SUCCESS, 
                '<strong>Congrats!</strong> your profile '
                'have been successfully update!', extra_tags='safe')
                return redirect('schedules:profile')
            else:
                return HttpResponse("Something terrible happened")
    # if a GET (or any other method) we'll create a blank form
    else:
        initial_data = {
            "first_name":current_user.first_name,
            "last_name":current_user.last_name,
            "phone_number":current_profile.phone,
            "address_1":current_profile.address_1,
            "address_2":current_profile.address_2,
            "city":current_profile.city,
            "state":current_profile.state,
            "zip_code":current_profile.zip_code,
            "country":current_profile.country 
        }
        form = UserProfileForm(initial=initial_data)
    return render(request, 'schedules/users/profile.html', {'form': form, 
        'current_profile':current_profile})

@login_required
def user_account(request):
    """Processing account update.
    """
    current_user = User.objects.get(pk=request.user.pk)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserAccountForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # authenticating user to proceed with updated
            check = authenticate(request, username=username, password=password)

            if form.modified_clean_username(request.user, username):
                # making sure username is not in use
                messages.add_message(request, messages.ERROR, 
                u"Username '%s' "
                 "is already in use." % username, extra_tags='safe')
                messages.add_message(request, messages.ERROR, 
                'To reset your password go to '
                '<strong>CHANGE PASSWORD</strong>', extra_tags='safe')
                return redirect('schedules:account')
            if check:
                # user has been authenticated
                is_updated = Profile.update_account(request.user, 
                **form.cleaned_data)

                # user has been authenticated, update it!
                messages.add_message(request, messages.SUCCESS, 
                '<strong>Congrats!</strong> your account '
                'have been successfully update!', extra_tags='safe')
                return redirect('schedules:account')
            else:
                # user could not be authenticated
                messages.add_message(request, messages.ERROR, 
                '<strong>Error!</strong> your account '
                'could not be authentitaced!', extra_tags='safe')
                messages.add_message(request, messages.ERROR, 
                'To reset your password go to '
                '<strong>CHANGE PASSWORD</strong>', extra_tags='safe')
                return redirect('schedules:account')
    # if a GET (or any other method) we'll create a blank form
    else:
        initial_data = {
            "username":current_user.username,
            "email":current_user.email
        }
        form = UserAccountForm(initial=initial_data)
    return render(request, 'schedules/users/account.html', {'form': form})
