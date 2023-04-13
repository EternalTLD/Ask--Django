from django.shortcuts import render

def home_page(request):
    return render(request, 'questions/index.html')

def question_detail(request):
    return render(request, 'questions/question.html')