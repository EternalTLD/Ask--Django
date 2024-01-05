from django.urls import path

from . import views


app_name = "api"

urlpatterns = [
    path(
        "questions/", views.QuestionViewSet.as_view({"get": "list", "post": "create"})
    ),
    path(
        "questions/<int:pk>/",
        views.QuestionViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
    path("users/", views.UserViewSet.as_view({"get": "list"})),
    path(
        "users/<int:pk>/",
        views.UserViewSet.as_view({"get": "retrieve", "put": "update"}),
    ),
    path("answers/", views.AnswerViewSet.as_view({"get": "list"})),
    path(
        "answers/<int:pk>/",
        views.AnswerViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
]
