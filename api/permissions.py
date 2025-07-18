from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users to edit objects.
    Non-admin users can only read objects.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # --> ('GET', 'HEAD', 'OPTIONS')
            return True
        return request.user and request.user.is_staff
