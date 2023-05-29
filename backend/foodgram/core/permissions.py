from rest_framework import permissions


class AuthorOrReadOnlyPermission(permissions.BasePermission):
    """Вносить изменения может только автор."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class ReadFileIsAuthenticatedPermission(permissions.BasePermission):
    """Скачивать список покупок может только
       аутентифицированный пользователь."""
    def has_permission(self, request, view):
        return request.user.is_authenticated
