from typing import cast
from django.db import IntegrityError
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated

from apps.api.v1.book.permissions import IsOwnerOrReadOnly
from apps.api.v1.book.services import get_user_bookmark
from apps.book.models import Book, Bookmark
from apps.book.utils import json_to_book
from apps.user.models import User

from .pagination import BookListPageNumberPagination, BookmarkPageNumberPagination
from .serializers import BookListCreateSerializer, BookRetrieveSerializer, BookmarkListSerializer, BookmarkRetrieveCreateSerializer

class GenericBook(generics.GenericAPIView):
    queryset = Book.objects.all().order_by('-id')
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookListCreate(generics.ListCreateAPIView, GenericBook):
    serializer_class = BookListCreateSerializer
    pagination_class = BookListPageNumberPagination
    
    def post(self, request, *args, **kwargs):    
        book = request.data.get('book')

        if not book or len(book) == 0:  
            data = {'book': 'Это поле не может быть пустым'}  
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

class OwnBookList(generics.ListAPIView, GenericBook):
    serializer_class = BookListCreateSerializer
    pagination_class = BookListPageNumberPagination
    
    def get_queryset(self):
        user_id = self.request.user.pk
        return self.queryset.filter(author_upload_id=user_id)
    
    
class BookRetrieve(generics.RetrieveAPIView, GenericBook):
    serializer_class = BookRetrieveSerializer
    pagination_class = None
    lookup_field = 'slug'   
    
    def get(self, request, page, *args, **kwargs):
        obj: Book = super().get_object()
        user = cast(User, self.request.user)
        url_page = page
        bookmark = get_user_bookmark(obj, user = user)
        serializer = self.get_serializer(obj)
        
        if bookmark:
            page = bookmark.get('target_page')
            
            if url_page == page:
                return Response(serializer.data)
            
            return redirect('books-retrieve', slug=obj.slug, page=page)
        
        return Response(serializer.data)

class BookmarkListCreate(generics.ListCreateAPIView):

    serializer_class = BookmarkListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = BookmarkPageNumberPagination

    def get_queryset(self):
        return Bookmark.objects.filter(user_id=self.request.user.pk).order_by('-id')

    def post(self, request, *args, **kwargs):
        user = request.user
        
        try:
            book = Book.objects.get(id=request.data['book_id'])
        except Book.DoesNotExist:
            data = {'details': 'Книга не найдена'}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        
        target_page = request.data['target_page']

        bookmark, is_created = Bookmark.objects.update_or_create(
            user=user,
            book=book,
            defaults={
                'target_page': target_page
            }
        )
        data = {"pk": bookmark.pk}
        
        if is_created:
            return Response(data=data, status=status.HTTP_201_CREATED)

        return Response(data=data, status=status.HTTP_200_OK)


class BookmarkDeleteView(generics.DestroyAPIView):
    queryset = Bookmark.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = "pk"