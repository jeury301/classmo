from django import template
from schedules.models import Session 
from datetime import datetime, timedelta, timezone
import calendar


register = template.Library() 


##in django template call function as
##{{ user|has_group:"group_name" }}
@register.filter(name='get_time_from_now') 
def get_time_from_now(Session_pk):
	print("this is my session_pk",Session_pk)
	session_pk=int(Session_pk)
	session=Session.objects.get(pk=session_pk)
	today=(datetime.now().weekday())
	today_time=datetime.now()
	h=(today_time.hour+today_time.minute/60)
	day=(session.start_date.weekday())
	day_hour=(session.start_date.hour+session.start_date.minute/60)
	order=(day-today)
	if order < 0: 
		order+=7
	day_return=int(order)
	hours=(day_hour-h)-4
	if hours < 0:
		day_return=6
		hours=24-abs(hours)

	hours=round(hours,0)
	hours = str(int(hours))
	if day_return==0:
		return "In {hours} hours".format(hours=hours)
	else:
		return "In {day_return} days and {hours} hours".format(day_return=day_return,hours=hours)
		

@register.filter(name='get_day_of_week') 
def get_day_of_week(Session_pk):
	session_pk=int(Session_pk)
	session=Session.objects.get(pk=session_pk)
	day=session.start_date.weekday()
	day_name=calendar.day_name[day]
	time=session.start_date.replace(tzinfo=timezone.utc).astimezone(tz=None).time().strftime('%I:%M %p')
	return "{day_name} at {time}".format(day_name=day_name,time=time)
	
	
    
