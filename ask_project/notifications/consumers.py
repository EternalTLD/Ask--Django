import json

from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope["url_route"]["kwargs"]["username"]
        self.notification_group_name = f"notification_{self.username}"

        await self.channel_layer.group_add(
            self.notification_group_name, 
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.notification_group_name, 
            self.channel_name
        )

    async def send_notification(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps(message))