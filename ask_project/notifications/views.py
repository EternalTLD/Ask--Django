from django.http import HttpResponseRedirect
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator

from .models import Notification


@method_decorator(login_required, name="dispatch")
class NotificationsListView(ListView):
    template_name = "notifications/notifications.html"
    context_object_name = "notifications"
    paginate_by = 20


class AllNotificationsListView(NotificationsListView):
    def get_queryset(self) -> QuerySet[Notification]:
        notifications = self.request.user.received_notifications.all()
        return notifications


class UnreadNotificationsListView(NotificationsListView):
    def get_queryset(self) -> QuerySet[Notification]:
        notifications = self.request.user.received_notifications.unread()
        return notifications


@require_POST
@login_required
def mark_as_read_view(request, id: int) -> HttpResponseRedirect:
    notification = get_object_or_404(Notification, id=id, to_user=request.user)
    notification.mark_as_read()
    return redirect("notifications:unread")


@require_POST
@login_required
def mark_all_as_read_view(request) -> HttpResponseRedirect:
    request.user.received_notifications.mark_all_as_read()
    return redirect("notifications:unread")
