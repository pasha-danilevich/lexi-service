from djoser.serializers import UserFunctionsMixin
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
from .serializers import BookmarkSerializer, SettingsPageSerializer, SettingsSerializer


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
    def activation(self, request, uid, token, *args, **kwargs):

        self.request.data.update(
            {
                "uid": uid,
                "token": token
            }
        )
        response = super().activation(request, *args, **kwargs)
        user = self.request.user
        user.activated_email = True
        user.save()
        return response

    @action(["post"], detail=False)
    def resend_activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user(is_active=True)  # set True

        if not settings.SEND_ACTIVATION_EMAIL:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if user:
            context = {"user": user}
            to = [get_user_email(user)]
            settings.EMAIL.activation(self.request, context).send(to)

        return Response(status=status.HTTP_204_NO_CONTENT)



class SettingsPageView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return SettingsSerializer
        else:
            return SettingsPageSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    def put(self, request, *args, **kwargs):
        instance = self.request.user.settings  # Получаем экземпляр настроек пользователя
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    
