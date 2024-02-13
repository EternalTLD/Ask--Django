from django.core.mail import send_mail
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@shared_task
def send_notification_task(notification: dict) -> None:
    """Handler to send push notification"""
    channel_layer = get_channel_layer()
    receiver = notification.get("to_user_username")
    async_to_sync(channel_layer.group_send)(
        f"notification_{receiver}",
        {
            "type": "send_notification",
            "notification": notification,
        },
    )


@shared_task
def send_email_notification_task(notification: dict) -> None:
    send_mail(
        "ASK-Notification",
        notification.get("message"),
        "ask@ask.com",
        [notification.get("to_user_email")],
    )
