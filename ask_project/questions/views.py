from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic.base import View
from django.views.generic import ListView, DetailView

from .models import Question, Category, Tag


class QuestionsView(View):
    """Questions list"""
    def get(self, request):
        questions = get_list_or_404(Question, draft=False)
        context = {'question_list': questions}
        return render(request, 'questions/index.html', context)
    
class QuestionsByCategoryView(View):
    """Question list by category"""
    def get(self, request, slug):
        category = get_object_or_404(Category, name=slug)
        questions = Question.objects.filter(category__name=slug)
        context = {'question_list': questions, 'category': category}
        return render(request, 'questions/by_category.html', context)
    
class QuestionsByTagView(View):
    """Question list by tag"""
    def get(self, request, slug):
        tag = get_object_or_404(Tag, title=slug)
        questions = Question.objects.filter(tags__title=slug)
        context = {'question_list': questions, 'tag': tag}
        return render(request, 'questions/by_tag.html', context)


class QuestionDetailView(DetailView):
    """Question detail"""
    model = Question
    slug_field = 'url'
    template_name = 'questions/question_detail.html'