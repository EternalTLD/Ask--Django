import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from notifications.services import send_answer_notification
from .models import Question, Answer


class AnswersConsumer(WebsocketConsumer):
    def connect(self) -> None:
        self.question_id = self.scope["url_route"]["kwargs"]["question_id"]
        self.question_group_name = f"question_{self.question_id}"

        async_to_sync(self.channel_layer.group_add)(
            self.question_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, code) -> None:
        async_to_sync(self.channel_layer.group_discard)(
            self.question_group_name, self.channel_name
        )

    def receive(self, text_data) -> None:
        text_data_json = json.loads(text_data)
        answer = text_data_json["text"]

        new_answer = self.create_new_answer(answer)
        data = {
            "author": new_answer.author.username,
            "date_published": new_answer.date_published.strftime("%d-%m-%Y"),
            "content": new_answer.content,
            "author_url": new_answer.author.profile.get_absolute_url(),
            "profile_image": new_answer.author.profile.get_profile_image(),
        }

        async_to_sync(self.channel_layer.group_send)(
            self.question_group_name, {"type": "new_answer", "message": data}
        )

    def new_answer(self, event) -> None:
        message = event["message"]
        self.send(text_data=json.dumps({"message": message}))

    def create_new_answer(self, text: str) -> Answer:
        question = Question.objects.get(id=int(self.question_id))
        answer = Answer.objects.create(
            question=question, author=self.scope["user"], content=text
        )
        send_answer_notification(answer=answer, question=question)
        return answer
