from typing import Any
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView

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

class UserLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('questions:home')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Неправильный email или пароль.')
        return self.render_to_response(self.get_context_data(form=form))

class UserLogoutView(LogoutView):
    template_name = 'users/logout.html'

