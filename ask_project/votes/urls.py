from django.urls import path

from .views import VoteView
from .models import Vote
from questions.models import Question, Answer


app_name = "votes"

urlpatterns = [
    path(
        "question/like/<int:pk>/",
        VoteView.as_view(model=Question, vote_type=Vote.LIKE),
        name="question_like",
    ),
    path(
        "question/dislike/<int:pk>/",
        VoteView.as_view(model=Question, vote_type=Vote.DISLIKE),
        name="question_dislike",
    ),
    path(
        "answer/like/<int:pk>/",
        VoteView.as_view(model=Answer, vote_type=Vote.LIKE),
        name="answer_like",
    ),
    path(
        "answer/dislike/<int:pk>/",
        VoteView.as_view(model=Answer, vote_type=Vote.DISLIKE),
        name="answer_dislike",
    ),
]
