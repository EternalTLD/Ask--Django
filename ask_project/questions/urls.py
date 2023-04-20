from django.urls import path, include

from . import views

urlpatterns = [
    path('<slug:slug>', views.QuestionDetail.as_view(), name='question_detail'),
    path('', views.Questions.as_view(), name='home'),
]