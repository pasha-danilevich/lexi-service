from django.shortcuts import redirect

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework import viewsets

from apps.api.v1.book.permissions import IsNotPrivetOrOwner, IsOwnerOrReadOnly
from apps.api.v1.book.services import get_user_bookmark
from apps.book.models import Book
from apps.book.utils import json_to_book
from apps.user.models import User

from .pagination import BookListPageNumberPagination
from .serializers import BookCreateSerializer, BookListSerializer, BookRetrieveSerializer


class BookViewSet(viewsets.ModelViewSet):
    pagination_class = BookListPageNumberPagination
    queryset = Book.objects.all().order_by('-id')
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['list', 'list_own_books']:
            return BookListSerializer
        elif self.action == 'create':
            return BookCreateSerializer
        elif self.action == 'retrieve':
            return BookRetrieveSerializer
        return super().get_serializer_class()
    
    def get_permissions(self):
        if self.action in ['retrieve', 'destroy']:
            return [IsNotPrivetOrOwner()] 
        return super().get_permissions() 


    def get_queryset(self):
        if self.action in ['retrieve', 'destroy']:
            return self.queryset
        elif self.action == 'list_own_books':
            user_id = self.request.user.pk
            return self.queryset.filter(author_upload_id=user_id)
        return self.queryset.filter(is_privet=False)
    
    def retrieve(self, request, page, *args, **kwargs):
        obj: Book = self.get_object()
        user = request.user
        bookmark = get_user_bookmark(obj, user=user)
        serializer = self.get_serializer(obj)

        if bookmark:
            bookmark_page = bookmark.get('target_page')
            
            if page == bookmark_page:
                return Response(serializer.data)

            return redirect('book-retrieve', slug=obj.slug, page=bookmark_page)

        return Response(serializer.data)
    
    def list_own_books(self, request):
        return super().list(request=request)




