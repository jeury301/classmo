from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from schedules.models import Profile

class UserRegistrationForm(forms.Form):
    """This form is used to capture and process user registration data
    """
    username = forms.CharField(label='User Name', 
        max_length=100, required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter username'}))
    email = forms.EmailField(label='Email', 
        max_length=100, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter email'}))
    password = forms.CharField(label='Password',
        max_length=100, required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
    password_repeat = forms.CharField(label='Password (again)',
        max_length=100, required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Re-enter password'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(u"Username '%s' "
            "is already in use." % username)

    def clean(self):
        """
        Verifies that the values entered into the password fields match

        NOTE: Errors here will appear in ``non_field_errors()`` 
        because it applies to more than one field.
        """
        cleaned_data = super(UserRegistrationForm, self).clean()
        if 'password' in self.cleaned_data and 'password_repeat' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password_repeat']:
                raise forms.ValidationError("Passwords don't match. "
                    "Please enter both fields again.")
        return self.cleaned_data



class UserProfileForm(forms.Form):
    """This form is used to capture the profile information about the user
    """
    first_name = forms.CharField(label="First Name", 
        max_length=100, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter first name'}),
        error_messages={'required': 'Please let us know what to call you!'})
    last_name = forms.CharField(label="Last Name", 
        max_length=100, required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter last name'}))
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', 
        message="Phone number must be entered in the format: "
        "'+999999999'. Up to 15 digits allowed.")
    phone_number = forms.CharField(validators=[phone_regex], 
        max_length=17, required=False,
        widget=forms.TextInput(attrs={'placeholder':'Enter phone number'})) 
    address_1 = forms.CharField(label="Address 1", max_length=100,
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter address 1'}))
    address_2 = forms.CharField(label="Address 2", max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter address 2'}))
    city = forms.CharField(label="City", max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter city'}))
    state = forms.CharField(label="State", max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter state'}))
    zip_code = forms.CharField(label="Zip code", max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter zip code'}))
    country = forms.CharField(label="Country", max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter country'}))


    def clean(self):
        """
        NOTE: Errors here will appear in ``non_field_errors()`` 
        because it applies to more than one field.
        """
        cleaned_data = super(UserProfileForm, self).clean()
        return self.cleaned_data


class UserAccountForm(forms.Form):
    """This form is used to capture and process user account data
    """
    username = forms.CharField(label='User Name', 
        max_length=100, required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter username'}))
    email = forms.EmailField(label='Email', 
        max_length=100, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter email'}))
    password = forms.CharField(label='Password',
        max_length=100, required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
    password_repeat = forms.CharField(label='Password (again)',
        max_length=100, required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Re-enter password'}))


    def clean(self):
        """
        Verifies that the values entered into the password fields match

        NOTE: Errors here will appear in ``non_field_errors()`` 
        because it applies to more than one field.
        """
        cleaned_data = super(UserAccountForm, self).clean()
        if 'password' in self.cleaned_data and 'password_repeat' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password_repeat']:
                raise forms.ValidationError("Passwords don't match. "
                    "Please enter both fields again.")
        return self.cleaned_data

    
    def modified_clean_username(self, user, username):
        try:
            user = User.objects.exclude(pk=user.pk).get(username=username)
        except User.DoesNotExist:
            return False
        return True
