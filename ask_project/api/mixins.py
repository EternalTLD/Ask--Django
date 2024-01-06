from rest_framework import serializers


class VoteCountFieldMixin(metaclass=serializers.SerializerMetaclass):
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()

    def get_likes(self, instance):
        return instance.votes.count_likes()
    
    def get_dislikes(self, instance):
        return instance.votes.count_dislikes()
