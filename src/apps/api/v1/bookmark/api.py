from django.shortcuts import get_object_or_404
from django.db.models import QuerySet, Q

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .pagination import BookmarkPageNumberPagination
from apps.book.models import Bookmark, Book

from .serializers import BookmarkListSerializer

class BookmarkViewSet(viewsets.ModelViewSet):
    serializer_class = BookmarkListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = BookmarkPageNumberPagination
    
    def filter_queryset(self, queryset: QuerySet):
        # Получаем параметр поиска из запроса
        search_query = self.request.query_params.get('search', None) # type: ignore

        if search_query:
            queryset = queryset.filter(
                Q(book__title__icontains=search_query) |
                Q(book__author__icontains=search_query)
            )
        return super().filter_queryset(queryset)

    def get_queryset(self):
        return Bookmark.objects.filter(user_id=self.request.user.pk).order_by('-id')

    def create(self, request, *args, **kwargs):
        user = request.user
        book = get_object_or_404(Book, id=request.data['book_id'])
        target_page = request.data['target_page']

        bookmark, is_created = Bookmark.objects.update_or_create(
            user=user,
            book=book,
            defaults={'target_page': target_page}
        )
        data = {"pk": bookmark.pk}

        if is_created:
            return Response(data=data, status=status.HTTP_201_CREATED)

        return Response(data=data, status=status.HTTP_200_OK)