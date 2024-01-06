from rest_framework import serializers


class VoteCountFieldMixin(metaclass=serializers.SerializerMetaclass):
    """Mixin adds likes and dislikes counter fields"""

    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()

    def get_likes(self, instance):
        return self._get_count(instance.votes, "likes")

    def get_dislikes(self, instance):
        return self._get_count(instance.votes, "dislikes")

    def _get_count(self, instance, method_name):
        try:
            return getattr(instance, f"count_{method_name}")()
        except AttributeError as exception:
            raise serializers.ValidationError(
                f"Error counting {method_name}: {exception}"
            )


class URIFieldMixin(metaclass=serializers.SerializerMetaclass):
    """Mixin builds an URI of object if object has url field or get_absolute_url method"""

    URI = serializers.SerializerMethodField()

    def get_URI(self, instance):
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
