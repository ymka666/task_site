from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *


class AddTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Tasks
        fields = ['title', 'content', 'deadline']


    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 10:
            raise ValidationError("Длинна превышает 200 символов")
        return title


class UpdateTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Tasks
        fields = ['title', 'content', 'deadline', 'status']

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError("Длинна превышает 200 символов")
        return title


class RegisterUserForm(UserCreationForm):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField()
    remember_me = forms.BooleanField(required=False)


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    content = forms.CharField()
    capatcha = CaptchaField()