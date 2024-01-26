from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("apps.users.urls", namespace="users")),
    path("profiles/", include("apps.profiles.urls", namespace="profiles")),
    path("notifications/", include("apps.notifications.urls", namespace="notifications")),
    path("api/v1/", include("apps.api.urls", namespace="api")),
    path("votes/", include("apps.votes.urls", namespace="votes")),
    path("", include("apps.questions.urls", namespace="questions")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
