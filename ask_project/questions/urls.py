from django.urls import path, include

from . import views

urlpatterns = [
    path('tags/<slug:slug>', views.QuestionsByTagView.as_view(), name='by_tag'),
    path('categories/<slug:slug>', views.QuestionsByCategoryView.as_view(), name='by_category'),
    path('<slug:slug>', views.QuestionDetailView.as_view(), name='question_detail'),
    path('', views.QuestionsView.as_view(), name='home'),
]