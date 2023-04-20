from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import ListView, DetailView

from .models import Question, Category


class Questions(View):
    """Questions list"""
    def get(self, request):
        questions = Question.objects.filter(draft=False)
        categories = Category.objects.all()
        context = {'question_list': questions, 'category_list': categories}
        return render(request, 'questions/index.html', context)

class QuestionDetail(DetailView):
    """Question detail"""
    model = Question
    slug_field = 'url'
    template_name = 'questions/question_detail.html'