from typing import Any

from django.db import models
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.utils.text import slugify
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Question, Answer
from .forms import AnswerForm, QuestionForm
from .mixins import AuthorRequiredMixin


User = get_user_model()


class QuestionsListView(generic.ListView):
    template_name = "questions/index.html"
    queryset = Question.published.get_all_questions()
    context_object_name = "questions_list"
    paginate_by = 10
    page_title = "Last questions"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.page_title
        return context


class QuestionsByTagListView(QuestionsListView):
    page_title = "Questions tagged #"

    def get_queryset(self) -> QuerySet[Question]:
        tag_slug = self.kwargs.get("tag_slug")
        return Question.published.get_tagged_questions(tag_slug)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"{self.page_title}{self.kwargs.get('tag_slug')}"
        return context


class PopularQuestionsListView(QuestionsListView):
    queryset = Question.published.get_popular_questions()
    page_title = "Popular questions"


class QuestionDetailView(generic.DetailView):
    template_name = "questions/question_detail.html"
    model = Question
    context_object_name = "question"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = AnswerForm()
        question = self.get_object()
        context["answers"] = Question.published.get_question_answers(question)
        context["similar_questions"] = Question.published.get_similar_questions(
            question
        )
        return context


class AnswerFormView(generic.detail.SingleObjectMixin, generic.FormView):
    template_name = "questions/question_detail.html"
    form_class = AnswerForm
    model = Answer

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.object = self.get_queryset()
        return super().post(request, *args, **kwargs)


class QuestionView(generic.View):
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        view = QuestionDetailView.as_view()
        question_id = self.kwargs.get("pk")
        Question.objects.filter(pk=question_id).update(views=models.F("views") + 1)
        return view(request, *args, **kwargs)

    @method_decorator(login_required())
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        view = AnswerFormView.as_view()
        form = AnswerForm(request.POST)
        if form.is_valid():
            question = Question.objects.get(id=self.kwargs["pk"])
            form.instance.author = request.user
            form.instance.question = question
            form.save()
        return view(request, *args, **kwargs)


class QuestionCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "questions/question_create_form.html"
    form_class = QuestionForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        title = form.cleaned_data.get("title")
        form.instance.slug = slugify(title)
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        question = self.object
        return reverse(
            "questions:detail", kwargs={"pk": question.id, "slug": question.slug}
        )


class QuestionUpdateView(AuthorRequiredMixin, generic.UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = "questions/question_update_form.html"
    context_object_name = "question"

    def get_success_url(self) -> str:
        return self.get_object().get_absolute_url()


class QuestionDeleteView(AuthorRequiredMixin, generic.DeleteView):
    model = Question
    success_url = "/"
    context_object_name = "question"


@require_GET
def question_search_view(request: HttpRequest) -> HttpResponse:
    results = []
    page_title = "Questions search"
    query = request.GET.get("query")

    if query:
        results = Question.published.search(query)
        page_title = f"Questions that contain {query}."

    return render(
        request,
        "questions/index.html",
        context={"page_title": page_title, "questions_list": results},
    )
