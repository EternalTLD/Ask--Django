from django.urls import path

from . import views


app_name = "profiles"

urlpatterns = [
    path("edit/", views.profile_edit_view, name="profile_edit"),
    path(
        "favorites/",
        views.UserFavoriteQuestionList.as_view(),
        name="favorite_questions",
    ),
    path("<slug:username>/", views.ProfileDetailView.as_view(), name="profile_detail"),
]
