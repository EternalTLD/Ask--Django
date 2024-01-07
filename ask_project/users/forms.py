from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.db import IntegrityError


User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
            "send_messages",
        )

    def clean_username(self) -> str:
        username = self.cleaned_data.get("username")
        if " " in username:
            raise forms.ValidationError("Username can't contains spaces.")
        return username

    def clean_email(self) -> str:
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email):
            raise forms.ValidationError("This email is already used.")
        return email

    def clean_password2(self) -> str:
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Password mismatch!")
        return password2

    def save(self, commit: bool = True) -> User:
        user = super(UserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data.get("first_name").capitalize()
        user.last_name = self.cleaned_data.get("last_name").capitalize()
        user.username = self.cleaned_data.get("username")
        user.email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password1")
        user.set_password(password)
        if commit:
            try:
                user.save()
            except IntegrityError:
                raise forms.ValidationError(
                    "User with this username or email already exists."
                )
        return user
