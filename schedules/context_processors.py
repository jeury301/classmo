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
    
    config = { }
    """"
    
    """
    

    # These are the default colors / language rendedred
    # by Django's template engine when there isn't a
    # corresponding value in the 'config' dictionary
    default_config = {
        "company": "Classmo",
        "primary_color": "#417690",
        "secondary_color": "#79aec8",
        "logo": "",
        "slogan": "Organize. Connect. Achieve.",
        "font-family": '"Roboto","Lucida Grande","DejaVu Sans","Bitstream Vera Sans",Verdana,Arial,sans-serif',
        "welcome_title": "Welcome to Classmo",
        "welcome_body": "Classmo is the place to succeed, click below to get registered!",
        "all_courses_body": "Here you can find all the courses available for regisration.  Click \"More Info\" to see sessions available for registration",
        "my_courses_body": "These are courses that you've registered for.  You can check your existing and past registrations, and register for new sessions.",
        "discussion_body": "Here you can ask questions and get answers for a variety of subjects",
        "primary_text_color": "#f5dd5d",
        "secondary_text_color": "#ffffff",
        "jumbotron_color":"#eceeef",
        "splash_images": {
        "images/splash_background1.jpg":"Photo by DAVID ILIFF. License: CC-BY-SA 3.0",
        "images/splash_background3.jpg":"Photo by Emgonzalez License: Public Domain",
        "images/splash_background2.jpg":"Photo by DAVID ILIFF. License: CC-BY-SA 3.0"
        }
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
