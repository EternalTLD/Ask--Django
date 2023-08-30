from rest_framework.generics import ListAPIView

from questions.models import Question, Answer
from profiles.models import Profile
from .serializers import QuestionsSerializer, AnswerSerializer, ProfileSerializer


class QuestionsListAPIView(ListAPIView):
    queryset = Question.published.all()
    serializer_class = QuestionsSerializer

class AnswersListAPIView(ListAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class ProfilesListAPIView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer