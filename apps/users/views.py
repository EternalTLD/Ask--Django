from django.shortcuts import render
from django.views.generic.edit import FormView
from django.http import HttpResponse
from django.contrib.auth import get_user_model

from .forms import UserRegistrationForm


User = get_user_model()


class UserRegistrationView(FormView):
    template_name = "users/registration.html"
    model = User
    form_class = UserRegistrationForm

    def form_valid(self, form: UserRegistrationForm) -> HttpResponse:
        user = form.save()
        return render(
            self.request, "users/registration_done.html", context={"user": user}
        )

    def form_invalid(self, form: UserRegistrationForm) -> HttpResponse:
        return render(self.request, "users/registration.html", context={"form": form})
