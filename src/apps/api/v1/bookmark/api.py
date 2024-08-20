from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.api.v1.book.permissions import IsOwnerOrReadOnly
from apps.api.v1.bookmark.pagination import BookmarkPageNumberPagination
from apps.book.models import Bookmark, Book

from .serializers import BookmarkListSerializer

class BookmarkViewSet(viewsets.ModelViewSet):
    serializer_class = BookmarkListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = BookmarkPageNumberPagination

    def get_queryset(self):
        return Bookmark.objects.filter(user_id=self.request.user.pk).order_by('-id')

    def create(self, request, *args, **kwargs):
        user = request.user

        try:
            book = Book.objects.get(id=request.data['book_id'])
        except Book.DoesNotExist:
            return Response({'details': 'Книга не найдена'}, status=status.HTTP_404_NOT_FOUND)

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

    def get_permissions(self):
        if self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        return super().get_permissions()