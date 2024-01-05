from rest_framework import viewsets
from rest_framework import permissions
from django.contrib.auth import get_user_model

from questions.models import Question, Answer
from . import serializers
from .permissions import IsAuthorOrReadOnly


User = get_user_model()


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.published.all()
    serializer_class = serializers.QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        question = self.get_object()
        question.views += 1
        question.save()
        return super().retrieve(request, *args, **kwargs)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = serializers.AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
