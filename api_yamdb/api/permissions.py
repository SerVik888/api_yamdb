from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Предоставляет полный доступ администратору,
    остальным пользователям даётся доступ только на чтение.
    """

    def has_permission(self, request, view):
        """
        Проверяет, что пользователь является администратором,
        либо метод безопасен.
        """
        return (
            request.method in SAFE_METHODS or (
                request.user.is_authenticated and request.user.role == 'admin'
            )
        )
