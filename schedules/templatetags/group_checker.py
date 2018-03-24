from django import template
from django.contrib.auth.models import Group 

register = template.Library() 


##in django template call function as
##{{ user|has_group:"group_name" }}
@register.filter(name='has_group') 
def has_group(user, group_name):
    group =  Group.objects.get(name=group_name) 
    return group in user.groups.all() 



