from typing import cast

from django.db.models import QuerySet

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.api.v1.stats.services import get_list_words, get_words_count_on_levels
from apps.api.v1.vocabulary.api import Vocabulary
from apps.word.managers import DictionaryQuerySet
from apps.word.models import Dictionary, Training
from apps.user.models import User
from config.settings import TRAINING_TYPES_ID



class RecentlyWord(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        user = self.request.user
        dictionary = Dictionary.objects.all(user.pk).order_by('-id')   
        data = get_list_words(dictionary=dictionary[:5])
        return Response(data=data)


class VocabularyStats(generics.ListAPIView, Vocabulary):

    def get_value(
        self,
        type_id: int,
        dictionary: DictionaryQuerySet,
        levels_length: int
    ):
        training_list = []

        for word in dictionary:
            word: Dictionary
            word_trainig = cast(QuerySet[Training], word.training)

            training_list.extend(word_trainig.filter(type_id=type_id))

        value = get_words_count_on_levels(
            levels_length=levels_length,
            training_list=training_list
        )

        return value

    def list(self, *args, **kwargs):
        user = cast(User, self.request.user)
        levels_length = len(user.settings.levels)
        dictionary = self.get_queryset()

        data = {
            type_name: self.get_value(type_id, dictionary, levels_length)
            for type_name, type_id in TRAINING_TYPES_ID.items()
        }

        return Response(data, status=status.HTTP_200_OK)
