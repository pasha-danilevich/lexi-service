from typing import Any
from django.http import Http404
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .utils import get_time_on_lvl, is_last_level_or_out, is_first_level
from apps.word.utils import get_current_unix_time

from apps.api.v1.vocabulary.serializers import UserWord
from .serializers import TrainingWordListSerializer


class Training(generics.GenericAPIView):
    queryset = UserWord.objects.all()
    serializer_class = TrainingWordListSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = None

    def __init__(self, **kwargs: Any) -> None:
        self.types = ['recognize', 'reproduce']
        super().__init__(**kwargs)

    def get_type(self):
        type = self.request.GET.get('type')
        if not type:
            detail = f'Необходимо передать параметр type: {self.types}'
            raise Http404(detail)
        elif type not in self.types:
            detail = f'Неизвестный тип: {type} Необходимо передать параметр type: {self.types}'
            raise Http404(detail)
        return type
    
    def create_filte(self, type: str ):
        # Формируем имя поля фильтрации для текущего типа тренировки
        filter_field = type + '_time' + '__lte'
        # Создаем фильтр для поиска тренировок
        filter = {
            "user_id": self.request.user.id,
            filter_field: get_current_unix_time()
        }
        return filter


class TrainingListUpdate(Training, generics.ListAPIView, mixins.UpdateModelMixin):

    def get_object(self):
        pk = self.request.data['pk']

        try:
            obj = UserWord.objects.get(id=pk)
        except:
            detail = f'Связь {pk} не найдена'
            raise Http404(detail)

        return obj

    def list(self, request, *args, **kwargs):
        type = self.get_type()
        user = self.request.user
        filter = self.create_filte(type=type)
        count_word_in_round = user.settings.count_word_in_round
        
        self.queryset = self.queryset.filter(**filter)[:count_word_in_round]

        if type == 'recognize':
            number_of_false_set = user.settings.number_of_false_set
            kwargs = {
                "many": True,
                "false_set": True,
                "number_of_false_set": number_of_false_set
            }
        elif type == 'reproduce':
            kwargs = {"many": True}

        serializer = self.get_serializer(self.queryset, **kwargs)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        type = self.get_type()
        instance = self.get_object()
        levels = self.request.user.settings.levels

        is_correct = self.request.data['is_correct']

        type_lvl = type + '_lvl'
        type_time = type + '_time'

        current_lvl = getattr(instance, type_lvl)
        
        if is_correct:
            if not is_last_level_or_out(levels, current_lvl):
                new_lvl = current_lvl + 1
            else:
                # остается на прежднем уровне (1й или последний)
                new_lvl = current_lvl
        else:
            if not is_first_level(current_lvl):
                new_lvl = current_lvl - 1
            else:
                # остается на прежднем уровне (1й или последний)
                new_lvl = current_lvl

        new_time = get_current_unix_time() + get_time_on_lvl(levels, new_lvl)

        setattr(instance, type_lvl, new_lvl)
        setattr(instance, type_time, new_time)

        instance.save(is_instance=True)

        return Response(status=status.HTTP_200_OK)


class TrainingInfo(Training):
    def get(self, request, *args, **kwargs):
        data = {}

        # Проходимся по всем типам тренировок
        for type in self.types:
            filter = self.create_filte(type)
            # Считаем количество тренировок для текущего типа
            count_word_to_training_recognize = self.queryset.filter(
                **filter).count()

            # Добавляем данные в словарь
            data.update(
                {f'count_word_to_training_{type}': count_word_to_training_recognize}
            )

        return Response(status=status.HTTP_200_OK, data=data)
