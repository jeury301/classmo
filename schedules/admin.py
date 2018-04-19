from django.contrib import admin
from django.forms.widgets import TextInput
from django import forms
from .models import Subject, Location, Session, Registration, Homework, Profile
from .models import Config

class SessionForm(forms.ModelForm):
    """A form model for Session

    Fields:
        inherited from Session through:
            fields = "__all__"
    """
    class Meta:
        model = Session
        fields = "__all__"

    def clean(self):
        """Validating start_date vs. end_date.
        - end_date must be greater than or equal to start_date
        """
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if start_date > end_date:
            raise forms.ValidationError("Dates are incorrect")
        return self.cleaned_data


class SessionAdmin(admin.ModelAdmin):
    """Overriding Session form on admin interface
    """
    form = SessionForm
    list_display = ('name', 'max_capacity', 'start_date', 'end_date')


class ConfigForm(forms.ModelForm):
    """A form model for Config
    """
    class Meta:
        model = Config
        fields = '__all__'
        widgets = {
            'primary_color': TextInput(attrs={'type': 'color'}),
            'secondary_color': TextInput(attrs={'type': 'color'}),
            'primary_text_color': TextInput(attrs={'type': 'color'}),
            'secondary_text_color': TextInput(attrs={'type': 'color'}),
            'jumbotron_color': TextInput(attrs={'type': 'color'})
        }

class ConfigAdmin(admin.ModelAdmin):
    form = ConfigForm



# Register your models here.
admin.site.register(Subject)
admin.site.register(Location)
admin.site.register(Session, SessionAdmin)
admin.site.register(Registration)
admin.site.register(Homework)
admin.site.register(Profile)
admin.site.register(Config, ConfigAdmin)
admin.site.site_header = 'Classmo Admin'





