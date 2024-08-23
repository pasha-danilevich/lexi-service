from typing import cast

from django.db import transaction
from django.http import Http404
from django.db.models import Subquery, OuterRef, QuerySet, Q

from rest_framework import generics,  status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.user.models import User
from apps.word.models import Dictionary

from .services import create_traning_for_word
from .serializers import DictionarySerializer, DictionaryListSerializer
from .pagination import VocabularyPageNumberPagination


class Vocabulary(generics.GenericAPIView):
    queryset = Dictionary.objects.all(None).order_by('-id')
    serializer_class = DictionarySerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = VocabularyPageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DictionarySerializer
        elif self.request.method == 'GET':
            return DictionaryListSerializer
        return self.serializer_class

    def get_user(self):
        user = cast(User, self.request.user)

        return user

    def get_queryset(self):
        user = self.get_user()
        user_id: int = user.pk

        return self.queryset.all(user_id=user_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        user = self.get_user()
        context['queryset'] = self.queryset.all(user_id=user.pk)
        return context


class VocabularyListCreate(generics.ListCreateAPIView, Vocabulary):

    def perform_create(self, serializer: DictionarySerializer):
        instance = serializer.save()
        return instance

    def create(self, request, *args, **kwargs):
        user = self.request.user
        data = self.request.data  # type: ignore
        data = {**data, 'user': user.pk}

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                instance = self.perform_create(serializer)
                create_traning_for_word(instance)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):

        user = self.request.user

        unique_words = (
            Dictionary.objects.filter(user_id=user.pk)
            .filter(word_id=OuterRef('word_id'))
            .order_by('word_id', '-date_added')
            .values('id')[:1]
        )

        words = Dictionary.objects.filter(
            user_id=user.pk,
            id__in=Subquery(unique_words)
        ).order_by('-date_added')

        return words

    def filter_queryset(self, queryset: QuerySet):
        # Получаем параметр поиска из запроса
        search_query = self.request.query_params.get( # type: ignore
            'search', None)

        if search_query:
            queryset = queryset.filter(
                Q(word__text__icontains=search_query) |
                Q(translation__text__icontains=search_query)
            )
        return super().filter_queryset(queryset)


class VocabularyDelete(generics.DestroyAPIView, Vocabulary):

    def get_object(self):
        data = self.request.data  # type: ignore
        try:
            instance = self.get_queryset().get(**data)
        except Dictionary.DoesNotExist:
            details = f'Связь {data} не найдена'
            raise Http404(details)
        return instance
