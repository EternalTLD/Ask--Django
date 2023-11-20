from django import template
from django.db.models import Count

from taggit.models import Tag
from ..models import Question


register = template.Library()


@register.simple_tag
def get_popular_tags():
    return (
        Tag.objects.filter(question__draft=False)
        .annotate(total_questions=Count("question"))
        .order_by("-total_questions")[:10]
    )


@register.filter
def count_taged_questions(tag_id):
    return Question.published.filter(tags=tag_id).count()


@register.filter
def shortify_question_content(content, limit=170):
    return content[:limit]
