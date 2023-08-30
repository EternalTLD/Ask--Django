from django.urls import path, include

from .views import (QuestionsListView, QuestionsByTagListView, PopularQuestionsListView,
                    QuestionCreateView, QuestionUpdateView, QuestionDeleteView,
                    QuestionView, question_search_view)

app_name = 'questions'

urlpatterns = [
    path('search/', question_search_view, name='question_search'),
    path('tags/<slug:tag_slug>/', QuestionsByTagListView.as_view(), name='by_tag'),
    path('popular/', PopularQuestionsListView.as_view(), name='popular_questions'),
    path('question/create/', QuestionCreateView.as_view(), name='question_create'),
    path('<int:pk>/<slug:slug>/', QuestionView.as_view(), name='question_detail'),
    path('update/<int:pk>/', QuestionUpdateView.as_view(), name="question_update"),
    path('delete/<int:pk>/', QuestionDeleteView.as_view(), name='question_delete'),
    path('', QuestionsListView.as_view(), name='home'),
]