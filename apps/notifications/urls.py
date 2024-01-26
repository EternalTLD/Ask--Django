from django.urls import path

from . import views

app_name = "notifications"

urlpatterns = [
    path("mark_as_read/<int:id>/", views.mark_as_read_view, name="mark_as_read"),
    path("mark_all_as_read/", views.mark_all_as_read_view, name="mark_all_as_read"),
    path("unread/", views.UnreadNotificationsListView.as_view(), name="unread"),
    path("", views.AllNotificationsListView.as_view(), name="all"),
]
