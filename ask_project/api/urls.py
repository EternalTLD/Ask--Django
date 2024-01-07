from rest_framework import routers
from django.urls import path, include

from . import views


app_name = "api"

router = routers.SimpleRouter()
router.register("users", views.UserViewSet)
router.register("questions", views.QuestionViewSet)
router.register("answers", views.AnswerViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
