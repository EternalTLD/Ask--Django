from django.urls import path

from . import views

app_name = "questions"

urlpatterns = [
    path("search/", views.question_search_view, name="question_search"),
    path("tags/<slug:tag_slug>/", views.QuestionsByTagListView.as_view(), name="by_tag"),
    path("popular/", views.PopularQuestionsListView.as_view(), name="popular_questions"),
    path("question/create/", views.QuestionCreateView.as_view(), name="question_create"),
    path("<int:pk>/<slug:slug>/", views.QuestionView.as_view(), name="question_detail"),
    path("update/<int:pk>/", views.QuestionUpdateView.as_view(), name="question_update"),
    path("delete/<int:pk>/", views.QuestionDeleteView.as_view(), name="question_delete"),
    path("", views.QuestionsListView.as_view(), name="home"),
]
