from django.urls import path

from .views import profile_edit_view, ProfileDetailView, UserFavoriteQuestionList

app_name = 'profiles'

urlpatterns = [
    path('edit/', profile_edit_view, name='profile_edit'),
    path('favorites/', UserFavoriteQuestionList.as_view(), name='favorite_questions'),
    path('<slug:username>/', ProfileDetailView.as_view(), name='profile_detail'),
]