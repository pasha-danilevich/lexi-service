from math import ceil
from typing import cast
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    
    def get_next_link(self):
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        return page_number
    
    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()
        if page_number == 1:
            return 1
        return page_number
    
    def get_paginated_response(self, data):
        page_size = cast(int, self.get_page_size(self.request))
        return Response({
            'page_count': ceil(self.page.paginator.count / page_size),
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })

