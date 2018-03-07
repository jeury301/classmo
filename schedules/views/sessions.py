from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse, Http404
from django.urls import reverse
from schedules.models import Session, Registration, Subject, User, Homework
from schedules.services.portal_tools import instructors_only, students_only
from django.contrib import messages

@login_required
@students_only
def registration(request,session_id):
    """
    Process's a registration, given user.pk as post, login is required. Comes from subject/session.html
    """
    sesh=get_object_or_404(Session,pk=session_id)
    user_id=request.POST.get("user_id")
    user_id=int(user_id)
    user=get_object_or_404(User,pk=user_id)
    reg=Registration(session=sesh,user=user)
    check=sesh.is_registered(user)
    if check:
        error = "You are already registered"
        messages.error(request, error)
        return render(request,'schedules/sessions/reg_success.html',{'session':sesh.id,'error':error})
    else:   
        registered_user = reg.save()
        print(": {}".format(registered_user))
        if not registered_user:
            error = "Sorry buddy, this session is full already!"
            messages.error(request, error)
            return redirect("schedules:session", session_id)
        messages.success(request, "Welcome to {}-{}".format(sesh.subject.name, sesh.name))
        return render(request,'schedules/sessions/reg_success.html',{'session':sesh.id})

@login_required
@students_only
def drop_session(request,session_id):
    """Drops session for a given user
    """
    try:
        registration_to_drop=Registration.student_registration_for_session(
            request.user.pk, session_id)
        registration_to_drop.delete()
    except Exception as e:
        raise Http404("ERROR: {}".format(e))
    return redirect("schedules:registrations")

@login_required
@students_only
def registrations(request):
    """Get's all user's registrations
    """
    student=request.user
    student_registrations = Registration.student_registrations(student)

    context = {
        "student":student,
        "student_registrations":student_registrations
    }
    return render(request, 'schedules/sessions/registrations.html', context)

@login_required
@students_only
def homework(request):
    """
    Gets all the user's HW assignments. They assignments are associated to a session, 
    which is associated to a user by a registration. Comes from schedules/users/index.html
    """
    user=request.user
    reg_list=user.registration_set.all()
    ass_list=[]
    for reg in reg_list:
        ass_list+=reg.session.homework_set.all() #this works???

    return render(request,'schedules/sessions/homeworks.html',{'assignments':ass_list,'user':user})

@login_required
@instructors_only
def assignments(request, request_type):
    """Show session assignemnts for current instructor
    """
    user=request.user
    my_sessions = ""
    all_sessions = ""

    if request_type == "all":
        # retrieve all sessions
        all_sessions = "active-link-blue"
        sessions = Session.objects.all()
    else:
        # retrieve all sessions for current instructor
        my_sessions = "active-link-blue"
        sessions = Session.instructor_assignments(user)

    context = {
        "sessions":sessions,
        "user":user,
        "my_sessions":my_sessions,
        "all_sessions":all_sessions
    }

    return render(request, 'schedules/sessions/assignments.html', context)
    