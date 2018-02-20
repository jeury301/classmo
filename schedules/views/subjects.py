from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.http import HttpResponse, Http404
from django.urls import reverse
from schedules.models import Subject, Session

def subjects(request):
    """
    List all subjects in the system
    """
    subjects = Subject.objects.all()
    context = {'subjects': subjects}
    return render(request, 'schedules/subjects/list.html', context)

def detail(request, subject_id):
    """
    Display details for a given subject.
    """
    context = {}
    try:
        subject = Subject.objects.get(pk=subject_id)
        context['subject'] = subject
    except Subject.DoesNotExist:
        raise Http404("Subject does not exist")

    # load current sessions for this subject
    sessions = Session.objects.filter(subject=subject_id)
    context['sessions'] = sessions
    return render(request, 'schedules/subjects/detail.html', context)

def sessions(request, subject_id):
    """
    Display sessions for a given subject.
    """
    context = {}
    try:
        subject = Subject.objects.get(pk=subject_id)
        sessions = Session.objects.filter(subject=subject_id)
        context['sessions'] = sessions
        context['subject'] = subject
    except Subject.DoesNotExist:
        raise Http404("Sessions does not exist")

    return render(request, 'schedules/subjects/sessions.html', context)

def session(request, session_id):
    """
    Display details for a given session of a subject.
    """
    context = {}
    try:
        session = Session.objects.get(pk=session_id)
        context['session'] = session
    except Subject.DoesNotExist:
        raise Http404("Session does not exist")

    return render(request, 'schedules/subjects/session.html', context)


