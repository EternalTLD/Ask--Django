from typing import Any
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView

from .models import Question, Category, Tag, Answer
from .forms import AnswerForm


class QuestionListView(ListView):
    template_name = 'questions/index.html'
    queryset = Question.published.all()
    context_object_name = 'question_list'
    paginate_by = 3

class QuestionsByCategoryView(View):

    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        questions = get_list_or_404(Question.published.filter(category__slug=slug))
        context = {'question_list': questions, 'category': category}
        return render(request, 'questions/by_category.html', context)
    
class QuestionsByTagView(View):

    def get(self, request, slug):
        tag = get_object_or_404(Tag, slug=slug)
        questions = get_list_or_404(Question.published.filter(tags__title=tag))
        context = {'question_list': questions, 'tag': tag}
        return render(request, 'questions/by_tag.html', context)

class QuestionDetailView(DetailView):
    template_name = 'questions/question_detail.html'
    model = Question
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AnswerForm()
        question = self.get_object()
        context['answers'] = question.answers.filter(active=True)
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
        form.instance.author_id = request.user.id
        form.instance.question = Question.objects.get(id=self.kwargs['id'])
        if form.is_valid():
            form.save()
        return view(request, *args, **kwargs)