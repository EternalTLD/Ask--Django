from django.urls import path, include
from .views import *

app_name = 'questions'

urlpatterns = [
    path('search/', question_search_view, name='question_search'),
    path('tags/<slug:tag_slug>/', QuestionsByTagView.as_view(), name='by_tag'),
    path('new_question/', NewQuestionView.as_view(), name='new_question'),
    path('vote/<str:action>/<int:id>/', add_question_vote_view, name='question_vote'),
    path('<int:id>/<slug:slug>/', QuestionView.as_view(), name='question_detail'),
    path('', QuestionListView.as_view(), name='home'),
]