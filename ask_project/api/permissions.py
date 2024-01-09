from rest_framework import permissions
from django.contrib.auth import get_user_model


User = get_user_model()


class IsAuthor(permissions.BasePermission):
    """
    Permission to only allow the author of an object to get access.

    This permission class checks whether the requesting user is the author of the
    object being accessed. If the object is a User instance, the permission is granted
    only if the requesting user matches the target User instance.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User):
            return request.user == obj
        return request.user == obj.author


class IsAuthorOrReadOnly(IsAuthor):
    """
    Permission to only allow the author of an object to edit it.

    This permission class extends the IsAuthor permission to also allow safe methods
    (GET, HEAD, OPTIONS) in addition to checking whether the requesting user is the author
    of the object.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return super().has_object_permission(request, view, obj)
