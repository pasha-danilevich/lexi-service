from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.api.v1.book.pagination import BookListPageNumberPagination
from apps.book.models import Book
from apps.book.utils import json_to_book

from apps.api.v1.book.serializers import BookSerializer, BookRetrieveSerializer

class BookListCreate(generics.ListCreateAPIView):
    queryset = Book.objects.all().order_by('-id')
    serializer_class = BookSerializer
    pagination_class = BookListPageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        user = self.request.user
        return serializer_class(*args, **kwargs, user=user)
    
    def post(self, request, *args, **kwargs):
        book = json_to_book(request.data['book'])
        request.data['book'] = book
        request.data['page_count'] = len(book)
        request.data['author_upload'] = request.user.id
        return super().post(request, *args, **kwargs)
    
class BookRetrieve(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookRetrieveSerializer
    pagination_class = None
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return Book.objects.get(slug=slug)

    def get(self, request, slug, page):
        queryset = self.get_queryset()
        user = self.request.user
        serializer = BookRetrieveSerializer(queryset, page=page, user=user)
        return Response(serializer.data)
    