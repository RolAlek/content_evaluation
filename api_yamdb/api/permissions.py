from rest_framework import permissions


class IsAuthorOrStaff(permissions.BasePermission):
    """
    Для анонимных пользователей доступны только безопасные методы.
    Права доступны только автору, модератору, администратору
    или администратору Django.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return (
                request.user == obj.author
                or request.user.is_superuser
                or request.user.is_admin
                or request.user.is_moderator
            )


class IsAdmin(permissions.BasePermission):
    """
    Права доступны только администратору или администратору Django.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.is_superuser
                or request.user.is_admin
            )


class ReadOnly(permissions.BasePermission):
    """Только безопасные методы."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
