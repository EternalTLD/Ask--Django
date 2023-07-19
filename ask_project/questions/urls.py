from django.urls import path, include
from .views import QuestionsByCategoryView, QuestionDetailView, QuestionsByTagView, QuestionListView, QuestionView

app_name = 'questions'

urlpatterns = [
    path('tags/<slug:slug>', QuestionsByTagView.as_view(), name='by_tag'),
    path('categories/<slug:slug>', QuestionsByCategoryView.as_view(), name='by_category'),
    path('<int:id>/<slug:slug>', QuestionView.as_view(), name='question_detail'),
    path('', QuestionListView.as_view(), name='home'),
]