from django.urls import path

from . import views

app_name = "questions"

urlpatterns = [
    path("", views.QuestionsListView.as_view(), name="home"),
    path("questions/popular/", views.PopularQuestionsListView.as_view(), name="popular"),
    path("questions/by_tag/<slug:tag_slug>/", views.QuestionsByTagListView.as_view(), name="by_tag"),
    path("questions/search/", views.question_search_view, name="search"),

    path("question/<int:pk>/<slug:slug>/", views.QuestionView.as_view(), name="detail"),
    path("question/create/", views.QuestionCreateView.as_view(), name="create"),
    path("question/update/<int:pk>/", views.QuestionUpdateView.as_view(), name="update"),
    path("question/delete/<int:pk>/", views.QuestionDeleteView.as_view(), name="delete"),
]
