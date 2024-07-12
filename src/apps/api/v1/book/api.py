from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated

from apps.book.models import Book, UserBook
from apps.book.utils import json_to_book

from .pagination import BookListPageNumberPagination, BookmarkPageNumberPagination
from .serializers import BookListCreateSerializer, BookRetrieveSerializer, BookmarkListSerializer, BookmarkRetrieveCreateSerializer

class GenaricBook(generics.GenericAPIView):
    queryset = Book.objects.all().order_by('-id')
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookListCreate(generics.ListCreateAPIView, GenaricBook):
    serializer_class = BookListCreateSerializer
    pagination_class = BookListPageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def post(self, request, *args, **kwargs):
        book = json_to_book(request.data['book'])
        request.data['book'] = book
        request.data['page_count'] = len(book)
        request.data['author_upload'] = request.user.id
        return super().post(request, *args, **kwargs)
    
class BookRetrieve(generics.RetrieveAPIView, GenaricBook):
    serializer_class = BookRetrieveSerializer
    pagination_class = None
    lookup_field = 'slug'
    


class BookmarkListCreate(generics.ListCreateAPIView, mixins.DestroyModelMixin):

    serializer_class = BookmarkListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = BookmarkPageNumberPagination

    def get_queryset(self):
        return UserBook.objects.filter(user_id=self.request.user.id).order_by('-id')

    def post(self, request, *args, **kwargs):
        user = request.user
        book = Book.objects.get(id=request.data['book_id'])
        target_page = request.data['target_page']

        obj, is_created = UserBook.objects.update_or_create(
            user=user,
            book=book,
            defaults={
                'target_page': target_page
            }
        )
        if is_created:
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_200_OK)


class BookmarkDestroy(generics.DestroyAPIView):
    queryset = UserBook.objects.all()
    serializer_class = BookmarkRetrieveCreateSerializer
    permission_classes = [IsAuthenticated]