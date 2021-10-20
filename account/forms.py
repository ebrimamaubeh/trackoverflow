from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 

# validators 
from django.core.validators import EmailValidator, RegexValidator

# heree. 
# https://www.ordinarycoders.com/blog/article/django-user-register-login-logout

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[EmailValidator])
    display_name = forms.CharField(max_length=20, required=True, validators=[RegexValidator])

    
    class Meta: 
        model = User 
        fields = ('display_name', 'email', 'username', 'password1', 'password2')

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.display_name = self.cleaned_data['display_name']
        if commit:
            user.save()

        return user 
