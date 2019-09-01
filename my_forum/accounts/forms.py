from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import PasswordInput


class SignUpForm(UserCreationForm):
    # email in from another model
    email=forms.CharField(max_length='254', required=True, widget=forms.EmailInput(attrs={'placeholder':'Email'}),
                          help_text="example@example.com")

    class Meta:
            model=User
            fields=['username','email','password1', 'password2']
            widgets = {
                'username': forms.TextInput(attrs={'placeholder': 'Username'}),
                   }

    def __init__(self, *args, **kwargs):
            super(SignUpForm, self).__init__(*args, **kwargs)
            self.fields['password1'].widget = PasswordInput(attrs={'class': 'form-control',
                                                                   'placeholder': 'Password '})
            self.fields['password2'].widget = PasswordInput(
                attrs={'class': 'form-control', 'placeholder': 'Password confirmation'})


class LoginForm(UserCreationForm):

    class Meta:
            model=User
            fields=['username','password']
