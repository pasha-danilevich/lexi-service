from typing import cast
from django.db import IntegrityError
from django.shortcuts import redirect

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics, status

from apps.api.v1.book.permissions import IsNotPrivetOrOwner, IsOwnerOrReadOnly
from apps.api.v1.book.services import get_user_bookmark
from apps.book.models import Book, Bookmark
from apps.book.utils import json_to_book
from apps.user.models import User

from .pagination import BookListPageNumberPagination
from .serializers import BookListCreateSerializer, BookRetrieveSerializer


class GenericBook(generics.GenericAPIView):
    queryset = Book.objects.all().order_by('-id')
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class BookListCreate(generics.ListCreateAPIView, GenericBook):
    serializer_class = BookListCreateSerializer
    pagination_class = BookListPageNumberPagination

    def post(self, request, *args, **kwargs):
        book = request.data.get('book')

        if not book or len(book) == 0:
            data = {'book': ['Это поле не может быть пустым']}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        book = json_to_book(request.data['book'])
        request.data['book'] = book
        request.data['page_count'] = len(book)
        request.data['author_upload'] = request.user.id

        try:
            return super().post(request, *args, **kwargs)
        except IntegrityError:
            data = {'details': 'Книга с таким название и автором уже существует'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        
    def get_queryset(self):
        return self.queryset.filter(is_privet=False)


class OwnBookList(generics.ListAPIView, GenericBook):
    serializer_class = BookListCreateSerializer
    pagination_class = BookListPageNumberPagination

    def get_queryset(self):
        user_id = self.request.user.pk
        return self.queryset.filter(author_upload_id=user_id)


class OwnBookDelete(generics.DestroyAPIView, GenericBook):
    lookup_field = 'pk'


class BookRetrieve(generics.RetrieveAPIView, GenericBook):
    serializer_class = BookRetrieveSerializer
    pagination_class = None
    lookup_field = 'slug'
    permission_classes = [IsNotPrivetOrOwner]

    def get(self, request, page, *args, **kwargs):
        obj: Book = super().get_object()
        user = cast(User, self.request.user)
        url_page = page
        bookmark = get_user_bookmark(obj, user=user)
        serializer = self.get_serializer(obj)

        if bookmark:
            page = bookmark.get('target_page')

            if url_page == page:
                return Response(serializer.data)

            return redirect('books-retrieve', slug=obj.slug, page=page)

        return Response(serializer.data)

