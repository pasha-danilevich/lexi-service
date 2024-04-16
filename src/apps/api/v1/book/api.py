# from rest_framework.permissions 
# from apps.api.v1.
from rest_framework import generics
from apps.book.models import Book
from apps.api.v1.book.serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = None
    
    