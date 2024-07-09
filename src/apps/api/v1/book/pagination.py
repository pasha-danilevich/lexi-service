from apps.api.v1.pagination import CustomPageNumberPagination


class BookPageNumberPagination(CustomPageNumberPagination):
    page_size = 10
    