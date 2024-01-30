from django.contrib.auth.forms import AuthenticationForm
from django import forms
from captcha.fields import CaptchaField
from orders.models import Orders


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))
    captcha = CaptchaField()


class Calendar(forms.Form):
    my_date_field = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Фильтр заказов на дату:'
    )


class DenialService(forms.ModelForm):
    denial_service = forms.ChoiceField(choices=Orders.DENIAL_SERVICE,
                                       widget=forms.Select(attrs={'id': 'denial_service', 'name': 'denial_service', 'class': 'form-control'}), label='')

    class Meta:
        model = Orders
        fields = ['denial_service']
