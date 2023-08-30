from django import template
from django.db.models import Count
from django.utils import timezone

from taggit.models import Tag
from ..models import Question, Answer


register = template.Library()

@register.simple_tag
def get_popular_tags():
    return Tag.objects.filter(question__draft=False).annotate(
        total_questions=Count('question')).order_by('-total_questions')[:10]

@register.simple_tag
def get_todays_popular_questions():
    today = timezone.now().date()
    return Question.published.filter(date_published__date=today).order_by('-views')[:5]

@register.filter
def count_taged_questions(tag_id):
    return Question.published.filter(tags=tag_id).count()

@register.filter
def shortify_question_content(content, limit=170):
    return content[:limit]

@register.filter
def count_question_likes(question_id):
    return Question.objects.filter(pk=question_id, votes__vote=1).count()

@register.filter
def count_question_dislikes(question_id):
    return Question.objects.filter(pk=question_id, votes__vote=-1).count()

@register.filter
def count_answer_likes(answer_id):
    return Answer.objects.filter(pk=answer_id, votes__vote=1).count()

@register.filter
def count_answer_dislikes(answer_id):
    return Answer.objects.filter(pk=answer_id, votes__vote=-1).count()