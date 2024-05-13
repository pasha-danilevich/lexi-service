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
    
        
    def post(self, request, *args, **kwargs):
        request_word = clean_string(self.request.data.get('word', ''))

        if not request_word:
            return Response(data='Слово не передано', status=status.HTTP_400_BAD_REQUEST)

        word_dict, fetch_response = fetch_word_data(request_word)
        if not fetch_response:
            return Response(data='Объект не найден и нет данных о слове', status=status.HTTP_400_BAD_REQUEST)
        
        fetch_response.update({'is_related_exists': False})
        
        word, created = Word.objects.get_or_create(
            text=request_word,
            defaults={**word_dict}
        ) 
        
        fetch_response.update(
            {
                'is_related_exists': word.user_related_with_word.exists(),
                'word_id': word.id
                }
            )
        
        return Response(fetch_response, status=status.HTTP_200_OK)


        
