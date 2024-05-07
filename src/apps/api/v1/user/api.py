from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from apps.user.models import UserBookRelation
from apps.book.models import Book
from .pagination import BookmarkPageNumberPagination
from .serializers import BookmarkSerializer

from djoser.views import UserViewSet
from djoser import signals
from djoser.conf import settings
from djoser.compat import get_user_email


class BookmarkListCreate(generics.ListCreateAPIView):
    
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = BookmarkPageNumberPagination
    
    def get_queryset(self):
        return UserBookRelation.objects.filter(user_id=self.request.user.id).order_by('-id')
    
    def post(self, request, *args, **kwargs):
        user = request.user
        book = Book.objects.get(id=request.data['book_id'])
        target_page = request.data['target_page']
        
        UserBookRelation.objects.update_or_create(
            user=user,
            book=book,
            defaults={
                'target_page': target_page
            }
        )

        return Response('f')
    
class UserActivate(UserViewSet):
    
    @action(["post"], detail=False)
    def activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.activated_email = True
        user.save()

        signals.user_activated.send(
            sender=self.__class__, user=user, request=self.request
        )

        if settings.SEND_CONFIRMATION_EMAIL:
            context = {"user": user}
            to = [get_user_email(user)]
            settings.EMAIL.confirmation(self.request, context).send(to)

        return Response(status=status.HTTP_204_NO_CONTENT)