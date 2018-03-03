from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from schedules.models import Profile
class UserRegistrationForm(forms.Form):
    first_name = forms.CharField(label="First Name", 
        max_length=100, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter first name'}),
        error_messages={'required': 'Please let us know what to call you!'})
    last_name = forms.CharField(label="Last Name", 
        max_length=100, required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter last name'}))
    email = forms.EmailField(label='Email', 
        max_length=100, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter email'}))
    username = forms.CharField(label='User Name', 
        max_length=100, required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter username'}))
    password = forms.CharField(label='Password',
        max_length=100, required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
    
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', 
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = forms.CharField(validators=[phone_regex], max_length=17) # validators should be a list    
    
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(u'Username "%s" is already in use.' % username)



