from rest_framework import permissions
from rest_framework.exceptions import MethodNotAllowed


class IsAdminOrSuperuser(permissions.BasePermission):
    """
    Проверяем является пользователь администратором или суперюзером."""

    def has_permission(self, request, view):
        if request.method == 'PUT':
            raise MethodNotAllowed(request.method)
        return (
            request.user
            and request.user.is_staff
            or not request.user.is_anonymous
            and request.user.role == "admin"
        )
