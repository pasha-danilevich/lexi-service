from typing import cast

from django.db.models import Count

from django.template.backends import django
from rest_framework import  status
from rest_framework.response import Response

from apps.api.v1.stats.services import create_lvl_list
from apps.api.v1.vocabulary.api import Vocabulary
from apps.user.models import User
from apps.word.models import Training
from config.settings import TRAINING_TYPES_ID



class RecentlyWord(Vocabulary):

    def get(self, request):     
        dictionary = self.get_queryset().select_related(
            'word', 
            'translation'
        ).values(
            'id', 
            'word__text',
            'translation__text', 
            'date_added'
        ).order_by('-date_added')[:5]
            
        data = word_list = [entry for entry in dictionary]
        return Response(data=data)


class VocabularyStats(Vocabulary):

    def get(self, *args, **kwargs):
        user = cast(User, self.request.user)
        levels_length = len(user.settings.levels)

        word_counts = (
            Training.objects
            .filter(dictionary__user_id=user.pk) 
            .values('type_id', 'lvl') 
            .annotate(word_count=Count('dictionary'))  
            .order_by('type_id', 'lvl')  # Сортируем по type_id и lvl
        )
        initial_list = [0 for _ in range(levels_length)]
        
        number_iteration = [0]  # Используем список для хранения значения
        word_counts = list(word_counts) # Используем список для хранения значения
        
        data = {
            type: create_lvl_list(
                counted_word=word_counts[number_iteration[0]:],  
                initial_list=list(initial_list),  # Создаем копию initial_list
                type_id=id,
                number_iteration=number_iteration
            )
            for type, id 
            in TRAINING_TYPES_ID.items()
        }

        return Response(data=data,  status=status.HTTP_200_OK)
