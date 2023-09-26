from typing import Any

from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User


class UserRegistrationForm(UserCreationForm):
     
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
        )

    def clean_username(self) -> str:
        username = self.cleaned_data['username']
        if ' ' in username:
            raise forms.ValidationError('Имя пользователя не должно содержать пробелы.')
        return username
    
    def clean_email(self) -> str:
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
    
    def save(self, commit: bool = True) -> Any:
        user = super(UserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data.get('first_name').capitalize()
        user.last_name = self.cleaned_data.get('last_name').capitalize()
        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password1')
        user.set_password(password)
        if commit:
            user.save()
        return user