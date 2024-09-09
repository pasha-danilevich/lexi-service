from typing import cast

from django.db import connection
from django.db import transaction
from django.http import Http404
from django.db.models import QuerySet, Q

from rest_framework import generics,  status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.api.v1.vocabulary.sql import get_query
from apps.user.models import User
from apps.word.models import Dictionary
from config.settings import TRAINING_TYPES

from .services import create_traning_for_word, get_params_dict, make_dict
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
        
        divisor = len(TRAINING_TYPES) # кол-во типов тренировок будет делителем для того, чтобы получить средний уровень для слова
        
        params = get_params_dict(self.request.query_params)  # type: ignore
        
        with connection.cursor() as cursor:
            cursor.execute(get_query(**params), [divisor, user.pk])
            result = cursor.fetchall()
            
        return make_dict(result)

    def filter_queryset(self, queryset: list):

        search_query = self.request.query_params.get( # type: ignore
            'search', None
        )
        
        filtered_queryset = []
        
        if search_query:   
            for item in queryset:
                if search_query in item['word_text']:
                    filtered_queryset.append(item)        
            return filtered_queryset
        
        return queryset
        
        


class VocabularyDelete(generics.DestroyAPIView, Vocabulary):

    def get_object(self):
        data = self.request.data  # type: ignore
        try:
            instance = self.get_queryset().get(**data)
        except Dictionary.DoesNotExist:
            details = f'Связь {data} не найдена'
            raise Http404(details)
        return instance
