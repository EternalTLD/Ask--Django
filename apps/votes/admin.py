from django.contrib.contenttypes.admin import GenericStackedInline

from .models import Vote


class VoteAdmin(GenericStackedInline):
    model = Vote
