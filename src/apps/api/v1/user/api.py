from typing import cast
from django.db import IntegrityError
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from djoser.views import UserViewSet

from djoser.conf import settings
from djoser.compat import get_user_email

from apps.user.models import User

from .serializers import SettingsPageSerializer, SettingsSerializer

from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class UserActivate(UserViewSet):

    def validate_email(self, email):
        try:
            validate_email(email)
        except ValidationError:
            return False
        return True
    
    def send_email(self, user):
        context = {"user": user}
        to = [get_user_email(user)]
        settings.EMAIL.activation(self.request, context).send(to)

    @action(["get"], detail=False)
    def activation(self, request, uid, token, *args, **kwargs):

        self.request.data.update(  # type: ignore
            {
                "uid": uid,
                "token": token
            }
        )
        response = super().activation(request, *args, **kwargs)
        user = cast(User, self.request.user)
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
            self.send_email(user)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False)
    def set_email(self, request, *args, **kwargs):

        user = cast(User, self.request.user)
        email: str = self.request.data.get('email', None)  # type: ignore

        if not email:
            return Response(data="Email не был передан", status=status.HTTP_400_BAD_REQUEST)

        if not self.validate_email(email):
            return Response(data="Некорректный email-адрес", status=status.HTTP_400_BAD_REQUEST)

        user.email = email
        user.activated_email = False

        try:
            user.save()
        except IntegrityError:
            return Response(data="Пользователь с таким email уже существует", status=status.HTTP_400_BAD_REQUEST)
        
        if user:
            self.send_email(user)
            
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
        user = cast(User, self.request.user)

        instance = user.settings  # Получаем экземпляр настроек пользователя
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()
