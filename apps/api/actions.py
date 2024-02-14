from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType

from apps.votes.models import Vote
from apps.notifications.services import send_vote_notification


class VoteActionsMixin:
    """
    Mixin providing like and dislike functionality for objects with voting capability.

    This mixin adds two actions (`add_like` and `add_dislike`) that allow users to
    vote (like or dislike) for a particular object.
    """

    @action(detail=True, methods=["post"])
    def add_like(self, request, pk):
        return self._vote(request.user, "like")

    @action(detail=True, methods=["post"])
    def add_dislike(self, request, pk):
        return self._vote(request.user, "dislike")

    def _vote(self, user, vote: str):
        obj = self.get_object()

        if vote == "like":
            vote_type = Vote.LIKE
        elif vote == "dislike":
            vote_type = Vote.DISLIKE

        if obj.votes.has_user_voted(user):
            vote_object = Vote.objects.get(
                content_type=ContentType.objects.get_for_model(obj),
                object_id=obj.id,
                user=user,
            )
            if vote_object.vote == vote_type:
                vote_object.delete()
                response_message = f"{vote} removed"
            else:
                Vote.objects.filter(pk=vote_object.pk).update(vote=vote_type)
                send_vote_notification(obj, vote_type, user)
                response_message = f"{vote} added"
        else:
            obj.votes.create(user=user, vote=vote_type)
            send_vote_notification(obj, vote_type, user)
            response_message = f"{vote} added"

        return Response(
            {"status": "success", "message": response_message},
            status=status.HTTP_200_OK,
        )