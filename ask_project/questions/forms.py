from django import forms
from .models import Answer, Question


class QuestionForm(forms.ModelForm):
    tags_list = forms.TextInput()
    class Meta:
        model = Question
        fields = ['title', 'category', 'tags' ,'content', 'draft']

class AnswerForm(forms.ModelForm):
    
    class Meta:
        model = Answer
        fields = ['content', ]

class SearchForm(forms.Form):
    query = forms.CharField()