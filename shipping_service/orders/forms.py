from orders.models import Orders
from captcha.fields import CaptchaField
from django import forms


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
