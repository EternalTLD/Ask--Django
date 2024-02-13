from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType

from apps.votes.models import Vote
from apps.notifications.services import send_vote_notification


class VoteCountFieldMixin(metaclass=serializers.SerializerMetaclass):
    """
    Mixin providing serializer fields for counting likes and dislikes.

    This mixin adds two serializer fields (`likes` and `dislikes`) to count the number
    of likes and dislikes for a given object.
    """

    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()

    def get_likes(self, instance):
        return self._get_count(instance.votes, "likes")

    def get_dislikes(self, instance):
        return self._get_count(instance.votes, "dislikes")

    def _get_count(self, instance, method_name):
        try:
            return getattr(instance, f"count_{method_name}")()
        except AttributeError as exception:
            raise serializers.ValidationError(
                f"Error counting {method_name}: {exception}"
            )


class URIFieldMixin(metaclass=serializers.SerializerMetaclass):
    """
    Mixin providing a serializer field for generating URIs.

    This mixin adds a serializer field (`URI`) to generate a URI for an object if it
    has either a `url` field or a `get_absolute_url` method.
    """

    URI = serializers.SerializerMethodField()

    def get_URI(self, instance):
        model = self.context["view"].get_serializer().Meta.model
        try:
            if hasattr(model, "get_absolute_url"):
                return self.context["request"].build_absolute_uri(
                    instance.get_absolute_url()
                )
            elif hasattr(model, "url"):
                return self.context["request"].build_absolute_uri(instance.url)
        except (AttributeError, ValueError) as exception:
            raise serializers.ValidationError(f"Error building URI: {exception}")


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

    def _vote(self, user, vote):
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
