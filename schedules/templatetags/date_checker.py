from django import template
from schedules.models import Session 
from datetime import timedelta
from django.utils import timezone
import calendar


register = template.Library() 


##in django template call function as
##{{ user|has_group:"group_name" }}
@register.filter(name='get_time_from_now') 
def get_time_from_now(Session_pk):
	##print("this is my session_pk",Session_pk)
	print(Session_pk,"SESSION_PK")
	
	session_pk=Session_pk
	session=Session.objects.get(pk=session_pk)
	today=(timezone.now())
	##today_time=datetime.now()
	##h=(today_time.hour+today_time.minute/60)
	session_start=session.start_date
	difference=session_start-today

	days=difference/(timedelta(days=1))
	

	
	if days < 0:
		return ""
	else:
		days=round(days,0)
		days=str(int(days))
		return "In {days} days ".format(days=days)
	

@register.filter(name='get_day_of_week') 
def get_day_of_week(Session_pk):
	session_pk=Session_pk
	session=Session.objects.get(pk=session_pk)
	day=session.start_date.weekday()
	day_name=calendar.day_name[day]
	time=session.start_date.replace(tzinfo=timezone.utc).astimezone(tz=None).time().strftime('%I:%M %p')
	return "{day_name} at {time}".format(day_name=day_name,time=time)
	
	
    
