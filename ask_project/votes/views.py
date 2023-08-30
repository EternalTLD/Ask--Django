from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType

from notifications.models import Notification
from questions.models import Answer, Question
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
                self.delete_vote_notification(obj)
                self.send_vote_notification(obj)
            else:
                vote_object.delete()
                self.delete_vote_notification(obj)
        except ObjectDoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
            self.send_vote_notification(obj)

        return HttpResponseRedirect(reverse('questions:home'))
    
    def send_vote_notification(self, obj):
        Notification.objects.create(
            from_user=self.request.user,
            to_user=obj.author,
            target_content_type=ContentType.objects.get_for_model(obj),
            target_object_id=obj.id,
            message=self.get_notification_message()
        )

    def get_notification_message(self):
        if self.model is Question:
            obj = 'вопрос'
        elif self.model is Answer:
            obj = 'ответ'
        if self.vote_type == 1:
            action = 'понравился'
        else:
            action = 'не понравился'
        return f'Пользователю {self.request.user.username} {action} ваш {obj}.'

    def delete_vote_notification(self, obj):
        notification = get_object_or_404(
            Notification,
            from_user=self.request.user,
            to_user=obj.author,
            target_content_type=ContentType.objects.get_for_model(obj),
            target_object_id=obj.id,
        )
        notification.delete()