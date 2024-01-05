from rest_framework import permissions
from django.contrib.auth import get_user_model


User = get_user_model()


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Permission to only allow author of an object to edit it"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if isinstance(obj, User):
            return request.user == obj
        return request.user == obj.author
