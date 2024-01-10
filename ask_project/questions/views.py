from typing import Any
from django.db.models import F
from django.db.models.query import QuerySet
from django.utils.text import slugify
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import TrigramSimilarity
from django.views import generic
from django.contrib.auth.decorators import login_required

from taggit.models import Tag
from .models import Question, Answer
from .forms import AnswerForm, QuestionForm, SearchForm
from .mixins import AuthorRequiredMixin


User = get_user_model()


class QuestionsListView(generic.ListView):
    template_name = "questions/index.html"
    queryset = Question.published.all()
    context_object_name = "questions_list"
    paginate_by = 10

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Last questions"
        return context


class QuestionsByTagListView(QuestionsListView):
    def get_queryset(self) -> QuerySet[Question]:
        tag_slug = self.kwargs.get("tag_slug")
        tag = get_object_or_404(Tag, slug=tag_slug)
        return Question.published.filter(tags__in=[tag])

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Questions tagged #{self.kwargs.get('tag_slug')}"
        return context


class PopularQuestionsListView(QuestionsListView):
    queryset = Question.published.get_popular_questions()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Popular questions"
        return context


class QuestionDetailView(generic.DetailView):
    template_name = "questions/question_detail.html"
    model = Question
    context_object_name = "question"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = AnswerForm()
        question = self.get_object()
        context["answers"] = question.answers.filter(active=True)
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
        Question.objects.filter(pk=question_id).update(views=F("views") + 1)
        return view(request, *args, **kwargs)

    @login_required
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        view = AnswerFormView.as_view()
        form = AnswerForm(request.POST)
        if form.is_valid():
            question = Question.objects.get(id=self.kwargs["pk"])
            form.instance.author = request.user
            form.instance.question = question
            form.save()
        return view(request, *args, **kwargs)


class QuestionCreateView(AuthorRequiredMixin, generic.CreateView):
    template_name = "questions/question_create_form.html"
    success_url = "/"
    form_class = QuestionForm

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = QuestionForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            form.instance.slug = slugify(title)
            form.instance.author_id = request.user.id
            form.save()
        return HttpResponseRedirect(
            reverse(
                "questions:detail",
                kwargs={"pk": form.instance.id, "slug": form.instance.slug},
            )
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


def question_search_view(request: HttpRequest) -> HttpResponse:
    form = SearchForm()
    query = None
    results = []
    page_title = "Questions search"

    if "query" in request.GET:
        form = SearchForm(request.GET)

        if form.is_valid():
            query = form.cleaned_data.get("query")
            results = (
                Question.published.annotate(
                    similarity=TrigramSimilarity("title", query)
                )
                .filter(similarity__gt=0.1)
                .order_by("-similarity")
            )
            page_title = f"Questions that contain {query}."

    return render(
        request,
        "questions/index.html",
        context={"page_title": page_title, "questions_list": results},
    )
