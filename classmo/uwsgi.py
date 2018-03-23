     1	"""
     2	WSGI config for classmo project.
     3	
     4	It exposes the WSGI callable as a module-level variable named ``application``.
     5	
     6	For more information on this file, see
     7	https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
     8	"""
     9	
    10	import os
    11	
    12	from django.core.wsgi import get_wsgi_application
    13	
    14	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "classmo.settings")
    15	
    16	application = get_wsgi_application()
