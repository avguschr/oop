# coding=utf-8
from django.contrib.auth.forms import UserCreationForm
from .models import User, Bid, Category
from django import forms


class RegisterForm(UserCreationForm):
    fio = forms.RegexField(label="ФИО", regex=r'^[а-яА-ЯёЁ\s-]+$', max_length=128,
                           error_messages={'invalid': 'Только символы русского алфавита.'},
                           help_text='Обязательное поле. Не более 128 символов. Только буквы русского алфавита.')

    agreement = forms.BooleanField(label='Согласие на обработку персональных данных', required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'fio',
            'email',
        )


class BidCreateForm(forms.ModelForm):
    name = forms.CharField(label='Название', max_length=128, help_text='Обязательное поле. Не более 128 символов.',
                           required=True)
    description = forms.CharField(max_length=1000, label='Описание', help_text='Обязательное поле.', required=True)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)
    img = forms.ImageField(required=True)

    class Meta:
        model = Bid
        fields = (
            'name',
            'description',
            'category',
            'img'
        )



