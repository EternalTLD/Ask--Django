from typing import Any, Mapping, Optional, Type, Union
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms.utils import ErrorList
from .models import User


class UserRegistrationForm(UserCreationForm):
     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Введите имя пользователя.'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Введите email.'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Введите пароль.'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Повторите пароль.'})

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )

    def clean_username(self):
        username = self.cleaned_data['username']
        if ' ' in username:
            raise forms.ValidationError('Имя пользователя не должно содержать пробелы.')
        if User.objects.filter(username=username):
            raise forms.ValidationError('Пользователь с таким никнеймом уже зарегистрирован.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email):
            raise forms.ValidationError('Пользователь с таким email-адресом уже зарегистрирован.')
        return email

    def clean_password2(self) -> str:
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Пароли не совпадают!')
        return password2
    
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user