from typing import Any
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

from .models import User
from .forms import UserRegistrationForm


class UserRegistrationView(CreateView):
    success_url = '/'
    template_name = 'users/registration.html'
    model = User
    form_class = UserRegistrationForm

    def get_success_url(self):
        return self.success_url
    
    def post(self, request, *args, **kwargs):
        if User.objects.filter(email=request.POST['username']):
            messages.warning(request, 'Пользователь уже зарегистрирован')
            return redirect('users:registration')

        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data.get('password1')
            user.set_password(password)
            user.save()
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('users:login')
        else:
            print(user_form.errors)
            return render(request, 'users/registration.html', context={'form': user_form})
