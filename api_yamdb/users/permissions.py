from rest_framework import permissions


class IsAdminOrSuperuser(permissions.BasePermission):
    """
    Проверяем является пользователь администратором или суперюзером."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )
