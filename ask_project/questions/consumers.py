import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Question, Answer


class AnswersConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.question_id = self.scope['url_route']['kwargs']['question_id']
        self.question_group_name = f'question_{self.question_id}'

        await self.channel_layer.group_add(
            self.question_group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.question_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        answer = text_data_json['text']

        new_answer = await self.create_new_answer(answer)
        data = {
            'author': new_answer.author.username,
            'date_published': new_answer.date_published.strftime('%Y-%m-%d'),
            'content': new_answer.content
        }

        await self.channel_layer.group_send(
            self.question_group_name,
            {
                'type': 'new_answer',
                'message': data
            }
        )

    async def new_answer(self, event):
        message = event['message']

        await self.send(
            text_data=json.dumps(
                {
                    'message': message
                }
            )
        )

    @database_sync_to_async
    def create_new_answer(self, text):
        question = Question.objects.get(id=int(self.question_id))
        new_answer = Answer.objects.create(
            question=question,
            author=self.scope['user'],
            content=text
        )
        return new_answer