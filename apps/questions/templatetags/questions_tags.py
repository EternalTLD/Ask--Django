from django import template

from ..models import Question


register = template.Library()


@register.simple_tag
def popular_tags_list():
    return Question.published.get_popular_tags()
