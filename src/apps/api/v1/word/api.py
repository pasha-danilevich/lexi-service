import inspect
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.api.v1.word.serializers import Word, WordSerializer

from config.settings import print_local_var
from .yandex_dictionary import fetch_word_data
from .utils import check_related_user, clean_string, get_or_create_word


class WordCreate(generics.GenericAPIView, mixins.CreateModelMixin):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request_word = clean_string(self.request.data.get('word', ''))
        user = self.request.user

        if not request_word:
            return Response(data='Слово не передано', status=status.HTTP_400_BAD_REQUEST)

        word = get_or_create_word(request_word)

        if not word:
            return Response(data='Объект не найден и нет данных о слове', status=status.HTTP_400_BAD_REQUEST)

        serializer = WordSerializer(word)

        response = {
            "word": serializer.data,
            'this_word_related_with_user': check_related_user(word=word, user=user)
        }

        return Response(response, status=status.HTTP_200_OK)
