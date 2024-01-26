import json

from django.db.models.query import QuerySet
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from .models import Notification


class NotificationConsumer(WebsocketConsumer):
    def connect(self) -> None:
        self.user = self.scope["user"]
        self.username = self.scope["url_route"]["kwargs"]["username"]
        self.notification_group_name = f"notification_{self.username}"

        async_to_sync(self.channel_layer.group_add)(
            self.notification_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code) -> None:
        async_to_sync(self.channel_layer.group_discard)(
            self.notification_group_name, self.channel_name
        )

    def receive(self, text_data) -> None:
        text_data_json = json.loads(text_data)
        if text_data_json["type"] == "show_unread_push_notifications":
            notifications = self.get_unread_notifications()
            notifications = [notification.to_json() for notification in notifications]

            async_to_sync(self.channel_layer.group_send)(
                self.notification_group_name,
                {
                    "type": "show_unread_push_notifications",
                    "notifications": notifications,
                    "count_notifications": len(notifications),
                },
            )
        elif text_data_json["type"] == "read_all_notifications":
            self.user.received_notifications.mark_all_as_read()
            async_to_sync(self.channel_layer.group_send)(
                self.notification_group_name,
                {
                    "type": "read_all_notifications",
                },
            )

    def get_unread_notifications(self) -> QuerySet[Notification]:
        notifications = self.user.received_notifications.unread()
        return notifications

    def send_notification(self, event) -> None:
        self.send(text_data=json.dumps(event))

    def show_unread_push_notifications(self, event) -> None:
        self.send(text_data=json.dumps(event))

    def read_all_notifications(self, event) -> None:
        self.send(text_data=json.dumps(event))
