from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from schedules.models import Session, Registration, Subject, User, Assignment

def sessions(request,session_id):
	"""
    Get's a session, this controller is probably redundent at this point. No html or view leads to this view
    """
	try:
		sesh = Session.objects.get(pk=session_id)
	except Session.DoesNotExist:
		return render(request,'schedules/sessions/session.html')
	reg_list=sesh.registration_set.all()
	return render(request,'schedules/sessions/session.html',{'session':sesh,'reg_list':reg_list})

@login_required
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
	# check2=sesh.is_instructor(user) #also might need to check if this user is instructor
	if check:
		return render(request,'schedules/sessions/reg_success.html',{'session':sesh.id,'error':"already exists"})
	else:	
		reg.save()
		return render(request,'schedules/sessions/reg_success.html',{'session':sesh.id})

@login_required
def assignments(request):
	"""
	Gets all the user's HW assignments. They assignments are associated to a session, 
	which is associated to a user by a registration. Comes from schedules/users/index.html
	"""
	user=request.user
	reg_list=user.registration_set.all()
	ass_list=[]
	for reg in reg_list:
		ass_list+=reg.session.assignment_set.all() #this works???

	return render(request,'schedules/sessions/assignments.html',{'assignments':ass_list,'user':user})




	