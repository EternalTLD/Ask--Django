from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Count
from django.utils.text import slugify
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import TrigramSimilarity
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView, CreateView
from taggit.models import Tag

from .models import Question, Category, Answer
from .forms import AnswerForm, QuestionForm, SearchForm

User = get_user_model()


class QuestionListView(ListView):
    template_name = 'questions/index.html'
    queryset = Question.published.all()
    context_object_name = 'question_list'
    paginate_by = 3

class QuestionsByTagView(ListView):
    template_name = 'questions/by_tag.html'
    queryset = Question.published.all()
    context_object_name = 'question_list'
    paginate_by = 3
     
    def get_queryset(self) -> QuerySet[Any]:
        tag_slug = self.kwargs.get('tag_slug')
        tag = get_object_or_404(Tag, slug=tag_slug)
        question_list = get_list_or_404(Question.published.filter(tags__in=[tag]))
        return question_list
    
class QuestionsByCategoryView(ListView):
    template_name = 'questions/by_category.html'
    queryset = Question.published.all()
    context_object_name = 'question_list'
    paginate_by = 3

    def get_queryset(self) -> QuerySet[Any]:
        category_slug = self.kwargs.get('category_slug')
        question_list = get_list_or_404(Question.published.filter(category__slug=category_slug))
        return question_list


class QuestionDetailView(DetailView):
    template_name = 'questions/question_detail.html'
    model = Question
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AnswerForm()
        question = self.get_object()
        context['answers'] = question.answers.filter(active=True)

        #similar questions by same tags
        question_tags_ids = question.tags.values_list('id', flat=True)
        similar_questions = Question.published.filter(tags__in=question_tags_ids).exclude(id=question.id)
        similar_questions = similar_questions.annotate(same_tags=Count('tags')).order_by('-same_tags', '-date_published')[:4]
        context['similar_questions'] = similar_questions
        return context
    
class AnswerFormView(SingleObjectMixin, FormView):
    template_name = 'questions/question_detail.html'
    form_class = AnswerForm
    model = Answer
    success_url = '#'

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_queryset()
        return super().post(request, *args, **kwargs)
    
class QuestionView(View):
    
    def get(self, request, *args, **kwargs):
        view = QuestionDetailView.as_view()
        return view(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        view = AnswerFormView.as_view()
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.instance.author_id = request.user.id
            form.instance.question = Question.objects.get(id=self.kwargs['id'])
            form.save()
        return view(request, *args, **kwargs)
    
class NewQuestionView(CreateView):
    template_name = 'questions/question_form.html'
    success_url = '/'
    form_class = QuestionForm

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        form = QuestionForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            form.instance.slug = slugify(title)
            form.instance.author_id = request.user.id
            form.save()
        return HttpResponseRedirect(reverse('questions:home'))
    
def question_search_view(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data.get('query')
            results = Question.published.annotate(
                similarity=TrigramSimilarity('title', query)
            ).filter(similarity__gt=0.1).order_by('-similarity')
    
    return render(request, 'questions/search.html', context={'form': form, 'query': query, 'results': results})

