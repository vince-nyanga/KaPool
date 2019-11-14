from rest_framework import permissions


class IsAuthenticatedUserOrReadOnly(permissions.BasePermission):
    """
    Object-level permission that allows users to edit only their own profiles.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user
