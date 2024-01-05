from rest_framework import serializers
from django.contrib.auth import get_user_model

from questions.models import Question, Answer
from profiles.models import Profile
from notifications.models import Notification


User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    """User profile serializer"""

    class Meta:
        model = Profile
        read_only_fields = ["rating"]
        exclude = ["user"]


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""

    profile = ProfileSerializer()
    questions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    answers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "profile",
            "questions",
            "answers",
        ]
        read_only_fields = ["username", "email", "questions", "answers"]

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.pop("last_name", instance.last_name)
        if hasattr(instance, "profile"):
            profile_data = validated_data.pop("profile", {})
            for k, v in profile_data.items():
                setattr(instance.profile, k, v)
        instance.save()
        return instance


class AnswerSerializer(serializers.ModelSerializer):
    """Answer serializer"""

    question_url = serializers.SerializerMethodField()
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Answer
        fields = "__all__"
        read_only_fields = ["date_published", "best_answer", "active", "url"]

    def get_question_url(self, instance):
        return self.context["request"].build_absolute_uri(instance.get_absolute_url())


class QuestionSerializer(serializers.ModelSerializer):
    """Question serializer"""

    url = serializers.SerializerMethodField()
    answers = AnswerSerializer(many=True)
    author = UserSerializer()

    class Meta:
        model = Question
        fields = "__all__"
        read_only_fields = [
            "url",
            "author",
            "date_published",
            "date_created",
            "date_updated",
            "views",
            "slug",
            "answers",
        ]

    def get_url(self, instance):
        return self.context["request"].build_absolute_uri(instance.get_absolute_url())


class NotificationSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    from_user = serializers.StringRelatedField()

    class Meta:
        model = Notification
        exclude = ["to_user"]

    def get_url(self, instance):
        return self.context["request"].build_absolute_uri(instance.url)
