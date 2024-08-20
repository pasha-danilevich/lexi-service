from rest_framework import permissions

from apps.book.models import Book

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
        if isinstance(obj, Book):
            return obj.author_upload == request.user
        
        return obj.user == request.user

class IsNotPrivetOrOwner(permissions.BasePermission):
    
    
    def has_object_permission(self, request, view, obj: Book):
        print(obj, obj.author_upload, request.user, obj.is_privet)
        if obj.author_upload == request.user:
            return True
        elif not obj.is_privet:
            return True
            