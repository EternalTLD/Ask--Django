from django.http import JsonResponse, HttpRequest
from django.views import View
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from notifications.services import send_vote_notification
from .models import Vote


class VoteView(View):
    model = None
    vote_type = None

    @transaction.atomic
    def post(self, request: HttpRequest, pk: int) -> JsonResponse:
        obj = get_object_or_404(self.model, pk=pk)
        user = request.user

        if obj.votes.has_user_voted(user):
            vote_object = Vote.objects.get(
                content_type=ContentType.objects.get_for_model(obj),
                object_id=obj.id,
                user=user,
            )
            if vote_object.vote == self.vote_type:
                vote_object.delete()
            else:
                Vote.objects.filter(pk=vote_object.pk).update(vote=self.vote_type)
                send_vote_notification(obj, self.vote_type, request.user)
        else:
            obj.votes.create(user=request.user, vote=self.vote_type)
            send_vote_notification(obj, self.vote_type, request.user)

        data = {
            "vote_type": self.vote_type,
            "total_likes": obj.votes.count_likes(),
            "total_dislikes": obj.votes.count_dislikes(),
        }

        return JsonResponse(data)
