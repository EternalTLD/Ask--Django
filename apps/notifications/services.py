from django.db.models import Model

from apps.questions.models import Answer, Question
from apps.users.models import User
from apps.notifications.tasks import (
    send_notification_task,
    send_email_notification_task,
)
from .models import Notification


def send_vote_notification(obj: Model, vote_type: int, user: User) -> None:
    if not hasattr(obj, "votes"):
        raise AttributeError(f"{obj} does not have votes attribute")

    action = "liked" if vote_type == 1 else "disliked"

    message = f"{user.username} {action} your {obj.__class__._meta.model_name}."

    if hasattr(obj, "get_absolute_url"):
        url = obj.get_absolute_url()
    elif hasattr(obj, "url"):
        url = obj.url
    else:
        url = None

    notification = Notification.objects.create(
        from_user=user,
        to_user=obj.author,
        message=message,
        url=url,
    )

    send_notification_task.delay(notification.to_json())
    send_email_notification_task.delay(notification.to_json())


def send_answer_notification(answer: Answer, question: Question) -> None:
    notification = Notification.objects.create(
        from_user=answer.author,
        to_user=question.author,
        message=f"New answer on {str(question)}",
        url=question.get_absolute_url(),
    )

    send_notification_task.delay(notification.to_json())
    send_email_notification_task.delay(notification.to_json())
