from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from schedules.models import Subject

def subjects(request):
    """
    List all subjects
    """
    subjects = Subject.objects.all()
    context = {'subjects': subjects}
    return render(request, 'schedules/subjects/list.html', context)