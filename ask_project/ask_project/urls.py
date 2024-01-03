from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls", namespace="users")),
    path("profiles/", include("profiles.urls", namespace="profiles")),
    path("notifications/", include("notifications.urls", namespace="notifications")),
    path("api/v1/", include("api.urls", namespace="api")),
    path("votes/", include("votes.urls", namespace="votes")),
    path("", include("questions.urls", namespace="questions")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
