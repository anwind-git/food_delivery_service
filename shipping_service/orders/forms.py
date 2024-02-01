from orders.models import Orders
from captcha.fields import CaptchaField
from django import forms
from django.conf import settings


class OrderCreateForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Orders
        fields = ['address', 'email', 'phone']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control', 'id': 'address', 'name': 'address',
                                              'placeholder': 'Адрес доставки'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'email', 'name': 'email',
                                             'placeholder': 'Электронная почта'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон'}),
        }


class DenialService(forms.ModelForm):
    denial_service = forms.ChoiceField(choices=settings.DENIAL_SERVICE,
                                       widget=forms.Select(attrs={'id': 'denial_service', 'name': 'denial_service', 'class': 'form-control'}), label='')

    class Meta:
        model = Orders
        fields = ['denial_service']


class Calendar(forms.Form):
    my_date_field = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Фильтр заказов на дату:'
    )
