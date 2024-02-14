from rest_framework import serializers


class VoteCountFieldMixin(metaclass=serializers.SerializerMetaclass):
    """
    Mixin providing serializer fields for counting likes and dislikes.

    This mixin adds two serializer fields (`likes` and `dislikes`) to count the number
    of likes and dislikes for a given object.
    """

    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()

    def get_likes(self, instance) -> int:
        return self._get_count(instance.votes, "likes")

    def get_dislikes(self, instance) -> int:
        return self._get_count(instance.votes, "dislikes")

    def _get_count(self, instance, method_name: str) -> int:
        try:
            return getattr(instance, f"count_{method_name}")()
        except AttributeError as exception:
            raise serializers.ValidationError(
                f"Error counting {method_name}: {exception}"
            )


class URIFieldMixin(metaclass=serializers.SerializerMetaclass):
    """
    Mixin providing a serializer field for generating URIs.

    This mixin adds a serializer field (`URI`) to generate a URI for an object if it
    has either a `url` field or a `get_absolute_url` method.
    """

    URI = serializers.SerializerMethodField()

    def get_URI(self, instance) -> str:
        model = self.context["view"].get_serializer().Meta.model
        try:
            if hasattr(model, "get_absolute_url"):
                return self.context["request"].build_absolute_uri(
                    instance.get_absolute_url()
                )
            elif hasattr(model, "url"):
                return self.context["request"].build_absolute_uri(instance.url)
        except (AttributeError, ValueError) as exception:
            raise serializers.ValidationError(f"Error building URI: {exception}")