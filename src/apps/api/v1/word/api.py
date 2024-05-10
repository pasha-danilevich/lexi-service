import inspect
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from apps.api.v1.word.serializers import WordSerializer, Word
from config.settings import print_local_var
from .yandex_dictionary import fetch_word_data
from .utils import clean_string


class WordCreate(generics.GenericAPIView, mixins.CreateModelMixin):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    lookup_field = 'text'
    
    def get_object(self, lookup_value: str):
        try:
            instance = self.queryset.get(**{self.lookup_field: lookup_value})
            return instance
        except Word.DoesNotExist:
            return None
        
    def post(self, request, *args, **kwargs):
        request_word = clean_string(self.request.data.get('word', ''))

        if not request_word:
            return Response(data='Слово не передано', status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object(request_word)

        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        word_dict = fetch_word_data(request_word)

        if word_dict:
            request.data.update(word_dict)
            return super().create(request, *args, **kwargs)

        return Response(data='Объект не найден и нет данных о слове', status=status.HTTP_400_BAD_REQUEST)
