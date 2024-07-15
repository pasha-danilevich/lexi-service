from typing import cast
from django.db import transaction

from rest_framework import generics,  status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.user.models import User

from .utils import create_traning_for_word, get_words_count_on_levels
from .serializers import DictionarySerializer, DictionaryListSerializer
from .pagination import VocabularyPageNumberPagination
from apps.word.models import Dictionary, TrainingType

from config.settings import TRAINING_TYPES

class Vocabulary(generics.GenericAPIView):
    queryset = Dictionary.objects.all().order_by('-id').prefetch_related('training')
    serializer_class = DictionarySerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = VocabularyPageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DictionarySerializer
        elif self.request.method == 'GET':
            return DictionaryListSerializer
        return self.serializer_class
    
    def get_queryset(self):
        queryset = self.queryset.filter(user_id=self.request.user.pk)
        return queryset


class VocabularyListCreate(generics.ListCreateAPIView, Vocabulary):
    
    
    def perform_create(self, serializer: DictionarySerializer):
        instance = serializer.save()
        return instance
    
    def create(self, request, *args, **kwargs):
        user = self.request.user
        data = self.request.POST.dict()
        data = {**data, 'user': user.pk}
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            with transaction.atomic():
                instance = self.perform_create(serializer)
                create_traning_for_word(instance)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
class VocabularyDelete(generics.DestroyAPIView, Vocabulary):
    lookup_field = 'pk'
    
    


class VocabularyStats(generics.ListAPIView, Vocabulary):

    def get_value(self, type, dictionary, levels_length):
        training_list = []
        
        for word in dictionary:
            training_list.extend(word.training.filter(type=type))
            
        value = get_words_count_on_levels(
            levels_length=levels_length,
            training_list=training_list
        )
        return value


    def list(self, *args, **kwargs):
        user = cast(User, self.request.user)
        levels_length = len(user.settings.levels)
        type_queryset = TrainingType.objects.all()
        dictionary = self.get_queryset()
        
        data = {type.name: self.get_value(type.pk, dictionary, levels_length) for type in type_queryset}

        return Response(data, status=status.HTTP_200_OK)
