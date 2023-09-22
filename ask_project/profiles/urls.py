from django.urls import path

from .views import profile_edit_view, ProfileDetailView

app_name = 'profiles'

urlpatterns = [
    path('edit/', profile_edit_view, name='profile_edit'),
    path('<slug:username>/', ProfileDetailView.as_view(), name='profile_detail'),
]