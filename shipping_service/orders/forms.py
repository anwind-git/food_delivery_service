from django.forms import ModelForm, TextInput, EmailInput
from .models import Orders


class OrderCreateForm(ModelForm):
    class Meta:
        model = Orders
        fields = ['address', 'email']

        widgets = {
            "address": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Адрес доставки',
                'Content - Type': 'application / json',
                'id': 'address',
                'name': "address"
            }),
            "phone": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Телефон',
                'Content - Type': 'application / json',
                'id': "phone",
                'name': "phone"
            }),
            "email": EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Электронная почта',
                'Content - Type': 'application / json',
                'id': "email",
                'name': "email",
                'type': "text"
            })
        }
        labels = {
            'address': '',
            'phone': '',
            'email': ''
        }
