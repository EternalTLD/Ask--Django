from django import template
from django.contrib.auth import get_user_model

from apps.questions.models import Question, Answer


User = get_user_model()
register = template.Library()


@register.filter
def count_user_questions(user_id):
    return Question.published.filter(author=user_id).count()


@register.filter
def count_user_answers(user_id):
    return Answer.objects.filter(author=user_id).count()


# @register.filter
# def count_user_recieved_likes(user_id):
#     questions = Question.published.filter(author=user_id)
#     question_likes = Question.votes.filter(object_id__in=questions, vote=1).count()
#     answers = Answer.objects.filter(author=user_id)
#     answer_likes = AnswerVote.objects.filter(vote_target__in=answers, vote=1).count()
#     return question_likes + answer_likes

# @register.filter
# def count_user_recieved_dislikes(user_id):
#     questions = Question.published.filter(author=user_id)
#     question_dislikes = QuestionVote.objects.filter(vote_target__in=questions, vote=-1).count()
#     answers = Answer.objects.filter(author=user_id)
#     answer_dislikes = AnswerVote.objects.filter(vote_target__in=answers, vote=-1).count()
#     return question_dislikes + answer_dislikes
