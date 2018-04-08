from schedules.services import portal_tools
from django.conf import settings


def global_context(request):
    """This function is used to create global context variables that could be
    used by any template.
    """
    current_user = request.user
    is_instructor = portal_tools.is_member(current_user, settings.GROUPS["INSTRUCTORS"])
    is_student = portal_tools.is_member(current_user, settings.GROUPS["STUDENTS"])
    
    role = "user"
    
    if is_instructor:
        role = "instructor"
    elif is_student:
        role = "student"
    elif current_user.is_staff:
        role = "staff"

    # global configuration object
    config = {"register_body":"My custom message"}

    global_context = {
        "current_user":current_user,
        "is_instructor":is_instructor,
        "is_student":is_student,
        "role":role,
        "config":config
    }           
    return global_context