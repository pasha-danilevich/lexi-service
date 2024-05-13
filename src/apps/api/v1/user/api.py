from rest_framework import generics, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from djoser.views import UserViewSet
from djoser import signals
from djoser.conf import settings
from djoser.compat import get_user_email

from apps.user.models import UserBookRelation, User
from apps.book.models import Book

from .pagination import BookmarkPageNumberPagination
from .serializers import BookmarkSerializer, SettingsSerializer, SettingsDictionarySerializer




class BookmarkListCreate(generics.ListCreateAPIView, mixins.DestroyModelMixin):
    
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

        return Response(status=status.HTTP_200_OK)
    
    
class BookmarkDestroy(generics.DestroyAPIView):
    queryset = UserBookRelation.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]
    
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
    
    
class UserSettings(generics.GenericAPIView):

    serializer_class = SettingsSerializer
    permission_classes = [IsAuthenticated]
    
    def get_user(self):
        return self.request.user
    
    def get(self, request, *args, **kwargs):
        user = self.get_user()
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
class UserSettingsDictionary(UserSettings):
    serializer_class = SettingsDictionarySerializer
    
    
    def put(self, request, *args, **kwargs):
        user = self.get_user()
        new_levels = self.request.data
        
        user.settings['levels'] = new_levels
        user.save()
        
        return Response(status=status.HTTP_200_OK)
    
    
