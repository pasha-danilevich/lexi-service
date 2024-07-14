import inspect
from rest_framework import generics,  status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .utils import get_words_count_on_levels
from .serializers import DictionarySerializer, DictionaryListSerializer
from .pagination import VocabularyPageNumberPagination
from apps.word.models import Dictionary

class Vocabulary(generics.GenericAPIView):
    queryset = Dictionary.objects.all().order_by('-id')
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
        queryset = self.queryset.filter(user_id=self.request.user.id)
        return queryset


class VocabularyListCreate(generics.ListCreateAPIView, Vocabulary):
    
    def create(self, request, *args, **kwargs):
        user = self.request.user
        self.request.data.update({'user': user.id})
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)

        if instance.id is None:
           return Response(serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        instance = serializer.save()
        return instance
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
class VocabularyDelete(generics.DestroyAPIView, Vocabulary):
    lookup_field = 'pk'
    
    


class VocabularyStats(generics.ListAPIView, Vocabulary):

    def get_value(self, type):
        user = self.request.user
        levels_length = len(user.settings.levels)

        user_words_queryset = self.get_queryset()
        value = get_words_count_on_levels(
            type=type + '_lvl',
            levels_length=levels_length,
            queryset=user_words_queryset
        )
        return value

    def list(self, request, *args, **kwargs):

        types = ('recognize', 'reproduce', )
        data = {type: self.get_value(type) for type in types}

        return Response(data, status=status.HTTP_200_OK)
