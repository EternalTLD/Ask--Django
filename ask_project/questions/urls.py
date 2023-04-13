from django.urls import path, include

from .views import home_page, question_detail

urlpatterns = [
    path('question/', question_detail),
    path('', home_page, name='home')
]