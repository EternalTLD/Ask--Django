from django.urls import path, include

from .views import QuestionsByCategoryView, QuestionDetailView, QuestionsByTagView, QuestionsView

app_name = 'questions'

urlpatterns = [
    path('tags/<slug:slug>', QuestionsByTagView.as_view(), name='by_tag'),
    path('categories/<slug:slug>', QuestionsByCategoryView.as_view(), name='by_category'),
    path('<slug:slug>', QuestionDetailView.as_view(), name='question_detail'),
    path('', QuestionsView.as_view(), name='home'),
]