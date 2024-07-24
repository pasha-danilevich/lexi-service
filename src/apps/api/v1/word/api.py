import inspect
from typing import cast
from rest_framework import generics, mixins, status
from rest_framework.response import Response

from apps.api.v1.word.serializers import Word, WordSerializer
from apps.user.models import User

from .services import get_related_pk, clean_string, get_or_create_word

class WordGeneric(generics.GenericAPIView):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    
    def update_data_with_word(self, data: dict, word: Word) -> dict:
        serializer = self.serializer_class(word)
        return {**data, "word": serializer.data}
    
    def update_data_with_related_pk(self, data: dict, new_data: list[int]):
        return {**data, 'related_pk': new_data}
    
class WordCreate(WordGeneric, mixins.CreateModelMixin):

    def post(self, request, *args, **kwargs):
        data = self.request.data # type: ignore
        request_word = clean_string(data.get('word', None)).lower()
        user = cast(User, self.request.user)

        if not request_word:
            return Response(data='Слово не передано', status=status.HTTP_400_BAD_REQUEST)
        
        try:
            word, created = get_or_create_word(request_word)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if not word:
            return Response(data='Объект не найден и нет данных о слове', status=status.HTTP_404_NOT_FOUND)
        
        data = {}
        data = self.update_data_with_word(data, word)
        
        if created:
            data = self.update_data_with_related_pk(data, new_data=[])
            return Response(data, status=status.HTTP_201_CREATED)
        
        if user.is_authenticated:
            related_pk = get_related_pk(word=word, user=user)
            data = self.update_data_with_related_pk(data, new_data=related_pk)


        return Response(data, status=status.HTTP_200_OK)
    
    
class WordGet(WordGeneric):

    def get(self, request, pk): 
        try:
            word = Word.objects.get(id=pk)
        except Word.DoesNotExist:
            return Response(data='Объект не найден и нет данных о слове либо был удален.', status=status.HTTP_404_NOT_FOUND)
        
        user = cast(User, self.request.user)
        
        
        data = {}
        data = self.update_data_with_word(data, word)
        
        if user.is_authenticated:
            related_pk = get_related_pk(word=word, user=user)
            data = self.update_data_with_related_pk(data, new_data=related_pk)
        
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
        translated_text = translation.text # type: ignore
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