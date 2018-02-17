from django.contrib import admin
from .models import Subject, Location, Session, Registration
# Register your models here.
admin.site.register(Subject)
admin.site.register(Location)
admin.site.register(Session)
admin.site.register(Registration)

