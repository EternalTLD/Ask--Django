from typing import Any
from django.shortcuts import render
from django.contrib import messages
from django.views.generic.edit import CreateView

from .models import User
from .forms import UserRegistrationForm
from profiles.models import Profile


class UserRegistrationView(CreateView):
    success_url = '/'
    template_name = 'users/registration.html'
    model = User
    form_class = UserRegistrationForm

    def get_success_url(self):
        return self.success_url
    
    def post(self, request, *args, **kwargs):
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
            Profile.objects.create(user=user)
            messages.success(request, 'Регистрация прошла успешно!')
            return render(request, 'users/registration_done.html', context={'user': user})
        else:
            print(user_form.errors)
            return render(request, 'users/registration.html', context={'form': user_form})
