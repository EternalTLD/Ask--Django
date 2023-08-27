from django.urls import path, include

from .views import (QuestionsListView, QuestionsByTagListView, PopularQuestionsListView,
                    QuestionCreateView, QuestionUpdateView, QuestionDeleteView,
                    QuestionView, VoteView, question_search_view)
from .models import Question, QuestionVote, Answer, AnswerVote

app_name = 'questions'

urlpatterns = [
    path('search/', question_search_view, name='question_search'),
    path('tags/<slug:tag_slug>/', QuestionsByTagListView.as_view(), name='by_tag'),
    path('popular/', PopularQuestionsListView.as_view(), name='popular_questions'),
    path('question/create/', QuestionCreateView.as_view(), name='question_create'),
    path(
        'question/like/<int:pk>/', 
        VoteView.as_view(
            model=Question, 
            vote_model=QuestionVote, 
            vote_type=QuestionVote.LIKE
        ), 
        name='question_like'
    ),
    path(
        'question/dislike/<int:pk>/', 
        VoteView.as_view(
            model=Question, 
            vote_model=QuestionVote, 
            vote_type=QuestionVote.DISLIKE
        ), 
        name='question_dislike'
    ),
    path(
        'answer/like/<int:pk>/', 
        VoteView.as_view(
            model=Answer, 
            vote_model=AnswerVote, 
            vote_type=AnswerVote.LIKE
        ), 
        name='answer_like'
    ),
    path(
        'answer/dislike/<int:pk>/', 
        VoteView.as_view(
            model=Answer, 
            vote_model=AnswerVote, 
            vote_type=AnswerVote.DISLIKE
        ), 
        name='answer_dislike'
    ),
    path('<int:pk>/<slug:slug>/', QuestionView.as_view(), name='question_detail'),
    path('update/<int:pk>/', QuestionUpdateView.as_view(), name="question_update"),
    path('delete/<int:pk>/', QuestionDeleteView.as_view(), name='question_delete'),
    path('', QuestionsListView.as_view(), name='home'),
]