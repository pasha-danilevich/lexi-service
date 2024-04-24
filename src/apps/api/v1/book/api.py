from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from apps.book.models import Book
from apps.api.v1.book.serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = PageNumberPagination
    
class BookRetrieve(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = None
    lookup_field = 'slug'
    