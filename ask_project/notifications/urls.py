from django.urls import path

from .views import (
    AllNotificationsListView,
    UnreadNotificationsListView,
    mark_as_read_view,
    mark_all_as_read_view,
)

app_name = "notifications"

urlpatterns = [
    path("mark_as_read/<int:id>/", mark_as_read_view, name="mark_as_read"),
    path("mark_all_as_read/", mark_all_as_read_view, name="mark_all_as_read"),
    path("unread/", UnreadNotificationsListView.as_view(), name="unread"),
    path("", AllNotificationsListView.as_view(), name="all"),
]
