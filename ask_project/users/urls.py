from django.urls import path
from django.contrib.auth.views import (LoginView, LogoutView, PasswordChangeView, 
                                       PasswordChangeDoneView, PasswordResetView, 
                                       PasswordResetDoneView,PasswordResetConfirmView, 
                                       PasswordResetCompleteView,)
from django.urls import reverse_lazy

from .views import UserRegistrationView

app_name = 'users'

urlpatterns = [
    path(
        'login/', 
        LoginView.as_view(
            redirect_authenticated_user = True,
            template_name = 'users/login.html',
        ), 
        name='login'),
    path(
        'logout/', 
        LogoutView.as_view(
            template_name = 'users/logout.html',
        ), 
        name='logout'
    ),
    path(
        'password-change/', 
         PasswordChangeView.as_view(
             success_url=reverse_lazy('users:password_change_done'),
             template_name='users/password_change_form.html',
            ), 
         name='password_change'
    ),
    path(
        'password-change/done/', 
         PasswordChangeDoneView.as_view(
             template_name='users/password_change_done.html',
             ), 
         name='password_change_done'
    ),
    path(
        'password-reset/', 
         PasswordResetView.as_view(
             template_name='users/password_reset_form.html',
             ), 
         name='password_reset'
    ),
    path(
        'password-reset/done/', 
         PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html',
             ), 
         name='password_reset_done'
    ),
    path(
        'password-reset/<uidb64>/<token>/', 
         PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html',
             ), 
         name='password_reset_confirm'
    ),
    path(
        'password-reset/complete/', 
         PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html',
             ), 
         name='password_reset_complete'
    ),
    path('registration/', UserRegistrationView.as_view() , name='registration'),
]