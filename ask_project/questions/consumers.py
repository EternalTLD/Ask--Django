import json

from django.contrib.contenttypes.models import ContentType
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from notifications.models import Notification
from .models import Question, Answer


class AnswersConsumer(WebsocketConsumer):

    def connect(self):
        self.question_id = self.scope['url_route']['kwargs']['question_id']
        self.question_group_name = f'question_{self.question_id}'

        async_to_sync(self.channel_layer.group_add)(
            self.question_group_name,
            self.channel_name
        )
        
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.question_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        answer = text_data_json['text']

        new_answer = self.create_new_answer(answer)
        data = {
            'author': new_answer.author.username,
            'date_published': new_answer.date_published.strftime('%d-%m-%Y'),
            'content': new_answer.content,
            'author_url': new_answer.author.profile.get_absolute_url(),
            'profile_image': new_answer.author.profile.get_profile_image()
        }
        print(data)

        async_to_sync(self.channel_layer.group_send)(
            self.question_group_name,
            {
                'type': 'new_answer',
                'message': data
            }
        )

    def new_answer(self, event):
        message = event['message']
        self.send(text_data=json.dumps(
            {
                'message': message
            }
        ))

    def create_new_answer(self, text):
        question = Question.objects.get(id=int(self.question_id))
        new_answer = Answer.objects.create(
            question=question,
            author=self.scope['user'],
            content=text
        )

        # Send notification to question author
        Notification.objects.create(
                from_user=new_answer.author, 
                to_user=question.author,
                target_content_type=ContentType.objects.get_for_model(question),
                target_object_id=question.id,
                message=f'Пользователь {new_answer.author} ответил на вопрос {question}',
                url=question.get_absolute_url()
            )
        
        return new_answer