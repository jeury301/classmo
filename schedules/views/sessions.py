from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from schedules.models import Session, Registration, Subject, User

def sessions(request,session_id):
	try:
		sesh = Session.objects.get(pk=session_id)
	except Session.DoesNotExist:
		return render(request,'schedules/sessions/session.html')

	reg_list=sesh.registration_set.all()

	return render(request,'schedules/sessions/session.html',{'session':sesh,'reg_list':reg_list})

def registration(request,session_id):
	sesh=get_object_or_404(Session,pk=session_id)
	user_id=request.POST.get("user_id")
	user_id=int(user_id)
	user=get_object_or_404(User,pk=user_id)
	reg=Registration(session=sesh,user=user)
	check=sesh.registration_set.filter(session=sesh,user=user).exists()
	if check:
		return render(request,'schedules/sessions/reg_success.html',{'session':sesh.id,'error':"already exists"})
	else:	
		reg.save()
		return render(request,'schedules/sessions/reg_success.html',{'session':sesh.id})



	