import inspect
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from config.settings import print_local_var
from .utils import get_words_count_on_levels
from .serializers import UserWord, UserWordSerializer


class Vocabulary(generics.GenericAPIView):
    queryset = UserWord.objects.all().order_by('-id')
    serializer_class = UserWordSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = None
    
    def get_queryset(self):
        queryset = self.queryset.filter(user_id = self.request.user.id)
        return queryset

class VocabularyListCreate(generics.ListCreateAPIView, Vocabulary):
    
    
    def create(self, request, *args, **kwargs):
        request_user_id = self.request.user.id
        request_word_id = self.request.data.get('word')
        
        self.request.data.update({'user': request_user_id})

        return super().create(request, *args, **kwargs)
        

class VocabularyStats(generics.ListAPIView, Vocabulary):
    
    def list(self, request, *args, **kwargs):
        user = self.request.user
        levels_length = user.settings.get('levels').__len__()
 
        data = {
            'recognize': get_words_count_on_levels('recognize_lvl', levels_length, self.queryset),
            'reproduce':get_words_count_on_levels('reproduce_lvl', levels_length, self.queryset)
        }
        return Response(data, status=status.HTTP_200_OK)
    
    