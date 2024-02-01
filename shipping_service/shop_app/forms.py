from django.contrib.auth.forms import AuthenticationForm
from django import forms
from captcha.fields import CaptchaField


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))
    captcha = CaptchaField()
