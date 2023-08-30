from django.urls import path

from .views import QuestionsListAPIView, AnswersListAPIView, ProfilesListAPIView


app_name = 'api'

urlpatterns = [
    path('questions_list/', QuestionsListAPIView.as_view()),
    path('answers_list/', AnswersListAPIView.as_view()),
    path('profiles_list/', ProfilesListAPIView.as_view())
]