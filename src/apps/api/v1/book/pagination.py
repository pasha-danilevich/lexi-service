from apps.api.v1.pagination import CustomPageNumberPagination


class BookListPageNumberPagination(CustomPageNumberPagination):
    page_size = 10
    
class BookmarkPageNumberPagination(CustomPageNumberPagination):
    page_size = 10