from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Пользовательское разрешение, которое позволяет владельцу объекта редактировать его,
    а всем остальным только просматривать.
    """

    def has_object_permission(self, request, view, training):
        # Чтение разрешений разрешено для любого запроса,
        # поэтому мы всегда разрешаем GET, HEAD или OPTIONS запросы.
        if request.method in permissions.SAFE_METHODS:
            return True

        dictionary = training.dictionary
        return dictionary.user == request.user