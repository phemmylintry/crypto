from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        print(obj.id)
        return obj.id == request.user


class UserHasToken(permissions.BasePermission):
    """User must be logged in"""

    def has_permission(self, request, view):
        return request.user.id is not None