from django.shortcuts import render
from django.views.generic.base import View

from .models import Question


class QuestionsView(View):
    """Questions list"""
    def get(self, request):
        questions = Question.objects.all()
        context = {'question_list': questions}
        return render(request, 'questions/index.html', context)