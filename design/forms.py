from django.contrib.auth.forms import UserCreationForm
from .models import User

from django import forms


class RegisterForm(UserCreationForm):
    fio = forms.RegexField(label="ФИО", regex=r'^[а-яА-ЯёЁ\s]+$', max_length=128,
                           error_messages={'invalid': 'Только символы русского алфавита.'},
                           help_text='Обязательное поле. Не более 128 символов. Только буквы русского алфавита.')

    class Meta:
        model = User
        fields = (
            'username',
            'fio',
            'email'
        )
