from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType

from notifications.models import Notification
from votes.models import Vote


class VoteView(View):
    model = None
    vote_type = None

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)

        try:
            vote_object = Vote.objects.get(
                content_type=ContentType.objects.get_for_model(obj),
                object_id=obj.id,
                user=request.user
            )
            if vote_object.vote is not self.vote_type:
                vote_object.vote = self.vote_type
                vote_object.save(update_fields=['vote'])
                # self.send_vote_notification(vote_target)
            else:
                vote_object.delete()
                # self.delete_vote_notification(vote_target)
        except ObjectDoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
            # self.send_vote_notification(vote_target)

        return HttpResponseRedirect(reverse('questions:home'))
    
    # def send_vote_notification(self, vote_target):
    #     Notification.objects.create(
    #         from_user=self.request.user,
    #         to_user=vote_target.author,
    #         question=self.get_vote_target_question(vote_target),
    #         type=self.get_notification_type(),
    #     )

    # def delete_vote_notification(self, vote_target):
    #     notification = get_object_or_404(
    #         Notification,
    #         from_user=self.request.user,
    #         to_user=vote_target.author,
    #         question=self.get_vote_target_question(vote_target),
    #         type=self.get_notification_type(),
    #     )
    #     notification.delete()