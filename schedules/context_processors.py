from django.conf import settings

from schedules.services import portal_tools


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

    # custom configurations
    config = {
    "company": "Yoga boga",
        "primary_color": "417690",
        "secondary_color": "79aec8",
        "logo": "",
        "slogan": "Strech",
        "font-family": '"Roboto","Lucida Grande","DejaVu Sans","Bitstream Vera Sans",Verdana,Arial,sans-serif',
        "welcome_title": "Welcome to Classmo",
        "welcome_body": "Classmo is the place to succeed, click below to get registered!",
        "all_courses_body": "Here you can find all the courses available for regisration.  Click \"More Info\" to see sessions available for registration",
        "my_courses_body": "These are courses that you've registered for.  You can check your existing and past registrations, and register for new sessions.",
        "discussion_body": "Here you can ask questions and get answers for a variety of subjects"
    }

    # These are the default colors / language rendedred
    # by Django's template engine when there isn't a
    # corresponding value in the 'config' dictionary
    default_config = {
        "company": "Classmo",
        "primary_color": "417690",
        "secondary_color": "79aec8",
        "logo": "",
        "slogan": "Organize. Connect. Achieve.",
        "font-family": '"Roboto","Lucida Grande","DejaVu Sans","Bitstream Vera Sans",Verdana,Arial,sans-serif',
        "welcome_title": "Welcome to Classmo",
        "welcome_body": "Classmo is the place to succeed, click below to get registered!",
        "all_courses_body": "Here you can find all the courses available for regisration.  Click \"More Info\" to see sessions available for registration",
        "my_courses_body": "These are courses that you've registered for.  You can check your existing and past registrations, and register for new sessions.",
        "discussion_body": "Here you can ask questions and get answers for a variety of subjects"
    }

    global_context = {
        "default_config": default_config,
        "current_user":current_user,
        "is_instructor":is_instructor,
        "is_student":is_student,
        "role":role,
        "config":config
    }           
   
    return global_context
