from django.urls import path

from .views import profile_edit_view

app_name = 'profiles'

urlpatterns = [
    path('edit/', profile_edit_view, name='profile_edit'),
]