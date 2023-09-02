from django.urls import re_path

from .consumers import AnswersConsumer

questions_websocket_urlpatterns = [
    re_path(r'questions/(?P<question_id>\d+)/$', AnswersConsumer.as_asgi())
]