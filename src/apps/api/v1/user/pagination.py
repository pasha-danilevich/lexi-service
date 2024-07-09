from rest_framework.pagination import PageNumberPagination

class BookmarkPageNumberPagination(PageNumberPagination):
    page_size = 10