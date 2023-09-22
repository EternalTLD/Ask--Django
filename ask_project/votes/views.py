from django.http import JsonResponse
from django.shortcuts import redirect
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
                self.create_vote_notifiction(obj)
            else:
                vote_object.delete()
        except ObjectDoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
            self.create_vote_notifiction(obj)

        data = {
            'vote_type': self.vote_type,
            'total_likes': obj.votes.count_likes(),
            'total_dislikes': obj.votes.count_dislikes(),
        }

        return JsonResponse(data)

    def create_vote_notifiction(self, obj):
        notification = Notification.objects.create(
            from_user=self.request.user,
            to_user=obj.author,
            target_content_type=ContentType.objects.get_for_model(obj),
            target_object_id=obj.id,
            message=self.get_vote_notification_message(obj),
            url=obj.get_absolute_url()
        )
        return notification

    def get_vote_notification_message(self, obj):
        if self.model is Question:
            target = 'вопрос ' + obj.title
        elif self.model is Answer:
            target = 'ответ на вопрос ' + obj.question.title

        if self.vote_type == 1:
            action = 'понравился'
        else:
            action = 'не понравился'
            
        return f'Пользователю {self.request.user.username} {action} ваш {target}.'