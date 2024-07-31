from typing import Dict, Optional, overload
from django.http import HttpRequest
from apps.book.models import Book, Bookmark
from apps.user.models import User
from config.settings import PAGE_SLICE_SIZE
from django.contrib.auth.models import AnonymousUser

def _get_page_from_context(context: dict[str, HttpRequest]) -> int:
    """
    Извлекает номер страницы из контекста запроса.
    
    Функция предполагает, что номер страницы передается в URL-адресе
    в качестве последнего элемента пути. Например:
    
    /some/path/2
    
    Где 2 - номер страницы.
    
    Args:
        context (dict[any, any]): Словарь контекста запроса.
        
    Returns:
        int: Номер страницы, извлеченный из контекста. Нумерация начинается с 0.
    """
    full_path = context['request'].get_full_path()
    page = int(full_path.split('/')[-1]) - 1
    return page

def get_start_end(context, obj: Book):
    """
    Функция рассчитывает начальную и конечную страницы для отображения на основе
    текущей страницы, извлеченной из контекста, и общего количества страниц в книге.
    
    Аргументы:
        context (dict): Словарь контекста запроса.
        obj (Book): Объект книги, для которой нужно рассчитать диапазон страниц.
        
    Возвращает:
        tuple: Кортеж, содержащий индекс начальной и конечной страницы для отображения.
    """
    page = _get_page_from_context(context=context)
    
    page_slice_size = PAGE_SLICE_SIZE
    
    start = (page // page_slice_size) * page_slice_size
    end = (page // page_slice_size) * page_slice_size + page_slice_size
    
    if end > obj.page_count:
        end = obj.page_count
    
    return (start, end)

@overload
def get_user_bookmark(obj, user: AnonymousUser) -> None:
    ...

@overload
def get_user_bookmark(obj, user: User) -> Dict[str, int]:
    ...

def get_user_bookmark(obj, user):
    """
    Аргументы:
        obj (Book): Объект книги.
        user (User): Объект пользователя.
        
    Возвращает:
        dict[str, int]: Словарь с полями pk и target_page, если пользователь не анонимный и объект Bookmark найден.
        None: Если пользователь анонимный или объект Bookmark не найден.
    """
    if user.is_anonymous:
        return None
    
    try:
        user_book = Bookmark.objects.get(book=obj, user=user)
        return {
            'pk': user_book.pk,
            'target_page': user_book.target_page
        }
    except Bookmark.DoesNotExist:
        return None