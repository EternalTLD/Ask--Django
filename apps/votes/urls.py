from django.urls import path

from apps.questions.models import Question, Answer
from . import models, views


app_name = "votes"

urlpatterns = [
    path(
        "question/like/<int:pk>/",
        views.VoteView.as_view(model=Question, vote_type=models.Vote.LIKE),
        name="question_like",
    ),
    path(
        "question/dislike/<int:pk>/",
        views.VoteView.as_view(model=Question, vote_type=models.Vote.DISLIKE),
        name="question_dislike",
    ),
    path(
        "answer/like/<int:pk>/",
        views.VoteView.as_view(model=Answer, vote_type=models.Vote.LIKE),
        name="answer_like",
    ),
    path(
        "answer/dislike/<int:pk>/",
        views.VoteView.as_view(model=Answer, vote_type=models.Vote.DISLIKE),
        name="answer_dislike",
    ),
]
