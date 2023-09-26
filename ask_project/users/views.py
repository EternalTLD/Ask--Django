from typing import Any

from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.http import HttpResponse, HttpRequest

from .models import User
from .forms import UserRegistrationForm


class UserRegistrationView(CreateView):
    template_name = 'users/registration.html'
    model = User
    form_class = UserRegistrationForm
    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            return render(request, 'users/registration_done.html', context={'user': user})
        
        return render(request, 'users/registration.html', context={'form': user_form})
