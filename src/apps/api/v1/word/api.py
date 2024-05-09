import inspect
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from apps.api.v1.word.serializers import WordSerializer, Word
from config.settings import print_local_var
from .yandex_dictionary import fetch_word_data


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
        request_word = self.request.data['word']
        word = fetch_word_data(request_word)
        instance = self.get_object(request_word)
        

        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(data=word)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

