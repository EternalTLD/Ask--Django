from django import template
from django.db.models import Count
from ..models import Question
from taggit.models import Tag

register = template.Library()

@register.simple_tag
def get_popular_tags():
    return Tag.objects.filter(question__draft=False).annotate(total_questions=Count('question')).order_by('-total_questions')[:10]
