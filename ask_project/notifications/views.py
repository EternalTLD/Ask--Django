from typing import Any
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Notification


class NotificationsListView(ListView):
    template_name = 'notifications/notifications.html'
    context_object_name = 'notifications'
    paginate_by = 20

    @method_decorator(login_required)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super(NotificationsListView, self).dispatch(request, *args, **kwargs)

class AllNotificationsListView(NotificationsListView):

    def get_queryset(self) -> QuerySet[Notification]:
        notifications = self.request.user.recieved_notifications.all()
        return notifications
    
class UnreadNotificationsListView(NotificationsListView):

    def get_queryset(self) -> QuerySet[Notification]:
        notifications = self.request.user.recieved_notifications.unread()
        return notifications

def mark_as_read_view(request, id: int) -> HttpResponseRedirect:
    if request.method == 'POST':
        notification = get_object_or_404(
            Notification, 
            id=id, 
            to_user=request.user
        )
        notification.mark_as_read()
    
    return redirect('notifications:unread')

def mark_all_as_read_view(request) -> HttpResponseRedirect:
    if request.method == 'POST':
        request.user.recieved_notifications.mark_all_as_read()

    return redirect('notifications:unread')
