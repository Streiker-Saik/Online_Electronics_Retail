from rest_framework.permissions import BasePermission


class IsActiveUser(BasePermission):
    """Право авторизованного и активного пользователя"""

    def has_permission(self, request, view):
        return request.user.is_active
