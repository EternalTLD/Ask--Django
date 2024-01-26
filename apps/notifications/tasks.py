from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@shared_task
def send_notification_task(notification: dict) -> None:
    """Handler to send notification"""
    channel_layer = get_channel_layer()
    username = notification.get("to_user_username")
    async_to_sync(channel_layer.group_send)(
        f"notification_{username}",
        {
            "type": "send_notification",
            "notification": notification,
        },
    )
