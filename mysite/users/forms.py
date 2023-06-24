from typing import Any, Optional
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from .models import User
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm

# if error occurs in captcha change the environment to "Python 3.11.3 64-bit" and of course you have to "pip install captcha"


class PasswordResetForm(PasswordResetForm):
    model = User
    fields = '__all__'

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)


class MyUserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g. John'}),
            'username': forms.TextInput(attrs={'placeholder': 'e.g. john'}),
            'email': forms.EmailInput(attrs={'placeholder': 'e.g. john@john.com'}),


        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(MyUserCreateForm, self).__init__(*args, **kwargs)

        for key, value in self.fields.items():
            value.widget.attrs.update({'class': 'input input--text'})

            self.fields['password1'].widget.attrs['placeholder'] = '••••••••'
            self.fields['password2'].widget.attrs['placeholder'] = '••••••••'


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio',
                  'social_twitter', 'social_linkedin', 'social_facebook']


class PasswordChangeForm(PasswordChangeForm):
    model = User
    fields = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

        for field in ['old_password', 'new_password1', 'new_password2']:
            self.fields[field].help_text = None
