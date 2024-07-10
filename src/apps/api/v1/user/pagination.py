from apps.api.v1.pagination import CustomPageNumberPagination

class BookmarkPageNumberPagination(CustomPageNumberPagination):
    page_size = 10