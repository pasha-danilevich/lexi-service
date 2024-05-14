import inspect
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.api.v1.word.serializers import WordSerializer, Word

from config.settings import print_local_var
from .yandex_dictionary import fetch_word_data
from .utils import clean_string


class WordCreate(generics.GenericAPIView, mixins.CreateModelMixin):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request_word = clean_string(self.request.data.get('word', ''))
        user = self.request.user
        if not request_word:
            return Response(data='Слово не передано', status=status.HTTP_400_BAD_REQUEST)

        word_dict, fetch_response = fetch_word_data(request_word)
        if not fetch_response:
            return Response(data='Объект не найден и нет данных о слове', status=status.HTTP_400_BAD_REQUEST)

        fetch_response.update({'this_word_related_with_user': False})

        word, created = Word.objects.get_or_create(
            text=request_word,
            defaults={**word_dict}
        )

        if word.related_users.exists() and user:

            user_related_word = user.related_words.all()

            if user_related_word.filter(word_id=word.id).exists():
                fetch_response.update(
                    {'this_word_related_with_user': True})


        fetch_response.update({'word_id': word.id})
        return Response(fetch_response, status=status.HTTP_200_OK)
