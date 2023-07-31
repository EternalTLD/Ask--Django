from django import template
from django.db.models import Count
from django.utils import timezone

from taggit.models import Tag
from ..models import Question


register = template.Library()

@register.simple_tag
def get_popular_tags():
    return Tag.objects.filter(question__draft=False).annotate(
        total_questions=Count('question')).order_by('-total_questions')[:10]

@register.simple_tag
def get_todays_popular_questions():
    today = timezone.now().date()
    return Question.published.filter(date_published__date=today).order_by('-views')[:5]
