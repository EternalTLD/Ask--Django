from typing import Any
from django import http
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from itertools import chain

from .models import Notification


class NotificationsListView(ListView):
    template_name = 'notifications/notifications.html'
    context_object_name = 'notifications'
    paginate_by = 20

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(NotificationsListView, self).dispatch(request, *args, **kwargs)

class AllNotificationsListView(NotificationsListView):

    def get_queryset(self) -> QuerySet[Any]:
        notifications = Notification.objects.recieved(self.request.user)
        return notifications
    
class UnreadNotificationsListView(NotificationsListView):

    def get_queryset(self) -> QuerySet[Any]:
        notifications = Notification.objects.unread(self.request.user)
        return notifications

def mark_as_read_view(request, id):
    if request.method == 'POST':
        notification = get_object_or_404(Notification, id=id, to_user=request.user)
        notification.mark_as_read()
    
    return redirect('notifications:unread')

def mark_all_as_read_view(request):
    if request.method == 'POST':
        Notification.objects.mark_all_as_read(request.user)

    return redirect('notifications:unread')
