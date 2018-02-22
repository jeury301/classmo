from django.contrib import admin
from .models import Subject, Location, Session, Registration, Assignment
# Register your models here.
admin.site.register(Subject)
admin.site.register(Location)
admin.site.register(Session)
admin.site.register(Registration)
admin.site.register(Assignment)

