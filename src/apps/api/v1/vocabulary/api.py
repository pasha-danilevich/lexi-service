import inspect
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from config.settings import print_local_var
from .utils import get_words_count_on_levels
from .serializers import UserWord, UserWordSerializer, UserWordListSerializer


class Vocabulary(generics.GenericAPIView):
    queryset = UserWord.objects.all().order_by('-id')
    serializer_class = UserWordSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = None

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserWordSerializer
        elif self.request.method == 'GET':
            return UserWordListSerializer
        return self.serializer_class
    
    def get_queryset(self):
        queryset = self.queryset.filter(user_id=self.request.user.id)
        return queryset


class VocabularyListCreate(generics.ListCreateAPIView, Vocabulary):

    def create(self, request, *args, **kwargs):
        request_user_id = self.request.user.id

        self.request.data.update({'user': request_user_id})

        return super().create(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


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
