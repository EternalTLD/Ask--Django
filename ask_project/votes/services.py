from django.db.models import Model

from notifications.models import Notification
from users.models import User


def create_vote_notification(obj: Model, vote_type: int, user: User) -> Notification:
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

    return notification
