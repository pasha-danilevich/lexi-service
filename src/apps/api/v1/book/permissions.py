from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Пользовательское разрешение, которое позволяет владельцу объекта редактировать его,
    а всем остальным только просматривать.
    """

    def has_object_permission(self, request, view, obj):
        # Чтение разрешений разрешено для любого запроса,
        # поэтому мы всегда разрешаем GET, HEAD или OPTIONS запросы.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешение на запись разрешено только владельцу объекта.
        
        try:
            return obj.user == request.user
        except AttributeError:
            return obj.author_upload == request.user