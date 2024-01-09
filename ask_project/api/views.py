from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from questions.models import Question, Answer
from notifications.models import Notification
from .permissions import IsAuthorOrReadOnly, IsAuthor
from .mixins import VoteActionsMixin
from . import serializers


User = get_user_model()


class QuestionViewSet(VoteActionsMixin, viewsets.ModelViewSet):
    queryset = Question.published.all()
    serializer_class = serializers.QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    @action(
        detail=True,
        methods=["post"],
        serializer_class=serializers.AnswerSerializer,
        permission_classes=[permissions.IsAuthenticated],
    )
    def add_answer(self, request, pk):
        """
        Add an answer to the specified question.
        """
        question = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(question=question, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def similar_questions(self, request, pk):
        """
        Get a list of similar questions to the specified question.
        """
        question = self.get_object()
        similar_questions = Question.published.get_similar_questions(question)
        serializer = self.get_serializer(similar_questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    @action(
        detail=True, methods=["get"], serializer_class=serializers.QuestionSerializer
    )
    def published_questions(self, request, pk):
        """
        Get a list of questions published by the specified user.
        """
        user = self.get_object()
        questions = Question.published.filter(author=user)
        serializer = self.get_serializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["get"],
        serializer_class=serializers.QuestionSerializer,
        permission_classes=[IsAuthor],
    )
    def all_questions(self, request, pk):
        """
        Get a list of all questions asked by the specified user.
        """
        user = self.get_object()
        questions = Question.objects.filter(author=user)
        serializer = self.get_serializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], serializer_class=serializers.AnswerSerializer)
    def answers(self, request, pk):
        """
        Get a list of answers provided by the specified user.
        """
        user = self.get_object()
        answers = Answer.objects.filter(author=user)
        serializer = self.get_serializer(answers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["get"],
        serializer_class=serializers.NotificationSerializer,
        permission_classes=[IsAuthor],
    )
    def notifications(self, request, pk):
        """
        Get a list of notifications for the specified user.
        """
        user = self.get_object()
        notifications = Notification.objects.filter(to_user=user)
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AnswerViewSet(VoteActionsMixin, viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = serializers.AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
