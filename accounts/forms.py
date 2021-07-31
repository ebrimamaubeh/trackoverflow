from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms 

from .models import Profile

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile 
        fields = ['biography', 'location', 'birth_date']