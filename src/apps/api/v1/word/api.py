import inspect
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.api.v1.word.serializers import Word, WordSerializer

from config.settings import print_local_var
from .yandex_dictionary import fetch_word_data
from .utils import get_related_pk, clean_string, get_or_create_word


class WordCreate(generics.GenericAPIView, mixins.CreateModelMixin):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    permission_classes = [IsAuthenticated]
    

    def post(self, request, *args, **kwargs):
        request_word = clean_string(self.request.data.get('word', None))
        user = self.request.user

        if not request_word:
            return Response(data='Слово не передано', status=status.HTTP_400_BAD_REQUEST)

        word = get_or_create_word(request_word)

        if not word:
            return Response(data='Объект не найден и нет данных о слове', status=status.HTTP_404_NOT_FOUND)

        serializer = WordSerializer(word)

        response = {
            "word": serializer.data,
            'related_pk': get_related_pk(word=word, user=user)
        }

        return Response(response, status=status.HTTP_200_OK)
    
    def get(self, request, pk, *args, **kwargs):
        word = get_or_create_word(id=pk)
        
        serializer = WordSerializer(word)
        data = serializer.data
        
        return Response(data, status=status.HTTP_200_OK)

from rest_framework.decorators import api_view
from googletrans import Translator

@api_view(['POST'])
def googletrans(request):
    text = request.data.get('text')
    if not text:
        return Response(data='Текст не передан', status=status.HTTP_400_BAD_REQUEST)

    dest_language = request.data.get('dest_language', 'ru')

    translator = Translator()

    try:
        translation = translator.translate(text, dest=dest_language)
        print(translation)
        translated_text = translation.text
        return Response({'translated_text': translated_text}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': f"Translation error: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
import requests

@api_view(['POST'])
def dictionaryapi(request):
    request_word = clean_string(request.data.get('word', None))
    
    if not request_word:
        return Response(data='Слово не передано', status=status.HTTP_400_BAD_REQUEST)
    
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{request_word}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return Response({'data': data}, status=status.HTTP_200_OK)
    
    return Response(data='Нет данных о слове', status=status.HTTP_404_NOT_FOUND)