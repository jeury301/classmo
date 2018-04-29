from django.conf import settings
from django.forms.models import model_to_dict

from schedules.services import portal_tools
from schedules.models import Config
import json

def global_context(request):
    """This function is used to create global context variables that could be
    used by any template.
    """
    current_user = request.user
    is_instructor = portal_tools.is_member(current_user, 
        settings.GROUPS["INSTRUCTORS"])
    is_student = portal_tools.is_member(current_user, 
        settings.GROUPS["STUDENTS"])

    role = "user"

    if is_instructor:
        role = "instructor"
    elif is_student:
        role = "student"
    elif current_user.is_staff:
        role = "staff"

    # custom configurations
    config = custom_config() 

    # These are the default colors / language rendedred
    # by Django's template engine when there isn't a
    # corresponding value in the 'config' dictionary
    default_config = {
        "company": "Classmo",
        "primary_color": "#417690",
        "secondary_color": "#79aec8",
        "logo": "",
        "slogan": "Organize. Connect. Achieve.",
        "font_family": ('"Roboto","Lucida Grande",'
            '"DejaVu Sans","Bitstream Vera Sans",Verdana,Arial,sans-serif'),
        "welcome_title": "Welcome to Classmo",
        "welcome_body": ("Classmo is the place to succeed, click below "
            "to get registered!"),
        "all_courses_body": ("Here you can find all the courses available for "
            "regisration.  Click \"More Info\" to see sessions available "
            "for registration"),
        "my_courses_body": ("These are courses that you've registered for. "
            "You can check your existing and past registrations, and register "
            "for new sessions."),
        "discussion_body": ("Here you can ask questions and get answers for a "
            "variety of subjects"),
        "primary_text_color": "#f5dd5d",
        "secondary_text_color": "#ffffff",
        "jumbotron_color":"#eceeef",
        "splash_images": {
            "images/splash_background1.jpg":("Photo by DAVID ILIFF. "
                "License: CC-BY-SA 3.0"),
            "images/splash_background3.jpg":("Photo by Emgonzalez. "
                "License: Public Domain"),
            "images/splash_background2.jpg":("Photo by DAVID ILIFF. "
                "License: CC-BY-SA 3.0")
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
        
    # printing all the global context
    # print(json.dumps({"config":config, "default_config":default_config}))

    return global_context


def custom_config():
    """Constructing an object with the active custom configuration
    """
    # splash image fields
    splash_fields = {
        "splash_url_1":"splash_license_1",
        "splash_url_2":"splash_license_2",
        "splash_url_3":"splash_license_3"
    }

    add_splash = True
    splash_images = {}

    # retrieving the first active custom configuration from db (latest modified)
    db_config = Config.objects.filter(
        is_active=True).order_by('-updated').first()

    # checking db contains an active configurations
    if db_config:
        # turning object into a dictionary
        custom_config = model_to_dict(db_config)

        # checking all splash images are passed into the object
        for field in splash_fields.keys():
            # if any splash field is empty, break out
            if (custom_config[field] == "" or 
                    custom_config[splash_fields[field]]== ""):
                # either splash url or splash license is empty
                add_splash = False
                break
            # both splash url and splash license are found
            # constructing splash_url:splash_license dict
            splash_images[custom_config[field]] = (
                custom_config[splash_fields[field]])

        # checking splash fields are ready to go
        if add_splash:
            # yes, all fields are found add it to final dict
            custom_config["splash_images"] = splash_images

        return custom_config

    # no active configuration exists
    return {}


