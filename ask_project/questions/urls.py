from django.urls import path, include
from .views import *

app_name = 'questions'

urlpatterns = [
    path('tags/<slug:tag_slug>', QuestionsByTagView.as_view(), name='by_tag'),
    path('categories/<slug:category_slug>', QuestionsByCategoryView.as_view(), name='by_category'),
    path('new_question/', NewQuestionView.as_view(), name='new_question'),
    path('<int:id>/<slug:slug>', QuestionView.as_view(), name='question_detail'),
    path('', QuestionListView.as_view(), name='home'),
]