from rest_framework import serializers
from django.contrib.auth import get_user_model
from taggit.serializers import TaggitSerializer, TagListSerializerField

from questions.models import Question, Answer
from profiles.models import Profile
from notifications.models import Notification
from .mixins import VoteCountFieldMixin, URIFieldMixin


User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for the Profile model."""

    class Meta:
        model = Profile
        read_only_fields = ["rating"]
        exclude = ["user"]


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model with associated Profile."""

    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "profile",
        ]
        read_only_fields = ["username"]

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.pop("last_name", instance.last_name)
        profile_data = validated_data.pop("profile", {})
        instance.profile, _ = Profile.objects.get_or_create(user=instance)
        for k, v in profile_data.items():
            setattr(instance.profile, k, v)
        instance.profile.save()
        instance.save()
        return instance


class AnswerSerializer(URIFieldMixin, VoteCountFieldMixin, serializers.ModelSerializer):
    """Serializer for the Answer model."""

    author = UserSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = "__all__"
        read_only_fields = ["date_published", "best_answer", "active", "question"]


class QuestionSerializer(
    URIFieldMixin,
    VoteCountFieldMixin,
    TaggitSerializer,
    serializers.ModelSerializer,
):
    """Serializer for the Question model."""

    answers = AnswerSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    tags = TagListSerializerField()

    class Meta:
        model = Question
        fields = "__all__"
        read_only_fields = [
            "date_published",
            "date_created",
            "date_updated",
            "views",
            "slug",
        ]


class NotificationSerializer(URIFieldMixin, serializers.ModelSerializer):
    """Serializer for the Notification model."""

    from_user = serializers.StringRelatedField()

    class Meta:
        model = Notification
        exclude = ["to_user", "url"]
