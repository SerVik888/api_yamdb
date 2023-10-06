from rest_framework import permissions
from rest_framework.exceptions import MethodNotAllowed


class IsAdminOrSuperuser(permissions.BasePermission):
    """
    Проверяем является пользователь администратором или суперюзером."""

    def has_permission(self, request, view):
        if request.method == 'PUT':
            raise MethodNotAllowed(request.method)
        return (
            not request.user.is_anonymous
            and request.user.is_admin
        )
