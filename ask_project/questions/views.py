from typing import Any, Dict
from django.db.models.query import QuerySet
from django.db.models import Count, F
from django.utils.text import slugify
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import TrigramSimilarity
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.core.exceptions import ObjectDoesNotExist

from taggit.models import Tag
from .models import Question, Answer
from notifications.models import Notification
from .forms import AnswerForm, QuestionForm, SearchForm

User = get_user_model()


class QuestionsListView(ListView):
    template_name = 'questions/index.html'
    queryset = Question.published.all()
    context_object_name = 'questions_list'
    paginate_by = 10

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Последние вопросы'
        return context

class QuestionsByTagListView(QuestionsListView):
     
    def get_queryset(self) -> QuerySet[Any]:
        tag_slug = self.kwargs.get('tag_slug')
        tag = get_object_or_404(Tag, slug=tag_slug)
        questions_list = get_list_or_404(Question.published.filter(tags__in=[tag]))
        return questions_list
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Вопросы с тегом {self.kwargs.get('tag_slug')}"
        return context
    
class PopularQuestionsListView(QuestionsListView):
    queryset = Question.published.order_by('-views', '-votes')
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Популярные вопросы'
        return context

class QuestionDetailView(DetailView):
    template_name = 'questions/question_detail.html'
    model = Question
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AnswerForm()
        question = self.get_object()
        context['answers'] = question.answers.filter(active=True)
        context['similar_questions'] = self.get_similar_questions(question)
        return context

    def get_similar_questions(self, question, limit=4):
        question_tags_ids = question.tags.values_list('id', flat=True)
        similar_questions = Question.published.filter(
            tags__in=question_tags_ids
        ).exclude(id=question.id)
        similar_questions = similar_questions.annotate(
            same_tags=Count('tags')
        ).order_by('-same_tags', '-date_published')[:limit]
        return similar_questions
    
class AnswerFormView(SingleObjectMixin, FormView):
    template_name = 'questions/question_detail.html'
    form_class = AnswerForm
    model = Answer
    success_url = '#'

    def post(self, request, *args, **kwargs):
        self.object = self.get_queryset()
        return super().post(request, *args, **kwargs)
    
class QuestionView(View):
    
    def get(self, request, *args, **kwargs):
        view = QuestionDetailView.as_view()
        question_id = self.kwargs.get('pk')
        Question.objects.filter(pk=question_id).update(views=F('views')+1)
        return view(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        view = AnswerFormView.as_view()
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        form = AnswerForm(request.POST)
        if form.is_valid():
            question = Question.objects.get(id=self.kwargs['pk'])
            form.instance.author_id = request.user.id
            form.instance.question = question
            form.save()

            # send notification to question author
            Notification.objects.create(
                from_user=request.user, 
                to_user=question.author,
                question=question,
                type='AQ'
            )
        return view(request, *args, **kwargs)
    
class QuestionCreateView(CreateView):
    template_name = 'questions/question_create_form.html'
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

class QuestionUpdateView(UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'questions/question_update_form.html'
    context_object_name = 'question'
    
    def get_success_url(self) -> str:
        return self.get_object().get_absolute_url()
    
class QuestionDeleteView(DeleteView):
    model = Question
    success_url = '/'
    context_object_name = 'question'
    
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