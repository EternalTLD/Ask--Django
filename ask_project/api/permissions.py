from rest_framework import permissions
from django.contrib.auth import get_user_model


User = get_user_model()


class IsAuthor(permissions.BasePermission):
    """Permission to only allow author of an object to get access"""

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User):
            return request.user == obj
        return request.user == obj.author


class IsAuthorOrReadOnly(IsAuthor):
    """Permission to only allow author of an object to edit it"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return super().has_object_permission(request, view, obj)
