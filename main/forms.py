from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True, label='Телефон (+7XXXXXXXXXX)')

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.startswith('+7') or not phone[1:].isdigit() or len(phone) != 12:
            raise forms.ValidationError('Телефон должен быть в формате +7XXXXXXXXXX')
        return phone