from schedules.services import portal_tools
from django.conf import settings


def global_context(request):
    """This function is used to create global context variables that could be
    used by any template.
    """
    current_user = request.user
    is_instructor = portal_tools.is_member(current_user, settings.GROUPS["INSTRUCTORS"])

    global_context = {
        "current_user":current_user,
        "is_instructor":is_instructor
    }           
    return global_context