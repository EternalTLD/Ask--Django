from django.urls import path, include
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy

from .views import UserRegistrationView, UserLoginView, UserLogoutView, dashboard

app_name = 'users'

urlpatterns = [
    path('registration/', UserRegistrationView.as_view() , name='registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('password-change/', PasswordChangeView.as_view(
        success_url=reverse_lazy('users:password_change_done'),
        template_name='users/password_change_form.html'
    ), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'
    ), name='password_change_done'),
    path('', dashboard, name='dashboard')

]