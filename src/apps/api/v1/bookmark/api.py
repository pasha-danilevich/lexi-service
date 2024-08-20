from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from apps.api.v1.book.permissions import IsOwnerOrReadOnly

from apps.book.models import Book, Bookmark

from .pagination import BookmarkPageNumberPagination
from .serializers import BookmarkListSerializer


class BookmarkListCreate(generics.ListCreateAPIView):

    serializer_class = BookmarkListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = BookmarkPageNumberPagination

    def get_queryset(self):
        queryset = (
            Bookmark.objects
            .filter(user_id=self.request.user.pk)
            .order_by('-id')
        )
        return queryset

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
