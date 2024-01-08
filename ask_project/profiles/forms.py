from django import forms

from users.models import User
from .models import Profile


class UserEditForm(forms.ModelForm):
    username = forms.CharField(disabled=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_image", "city", "country", "status"]
