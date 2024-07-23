from typing import Any, Type, Union, cast
from django.http import Http404
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.api.v1.training.serializers import RecognizeListSerializer, ReproduceListSerializer
from apps.user.models import User

from .utils import get_time_on_lvl, is_last_level_or_out, is_first_level
from apps.word.utils import get_current_unix_time

from apps.word.models import Dictionary, Training


from config.settings import TRAINING_TYPES


class TrainingView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]
    pagination_class = None

    def __init__(self, **kwargs: Any) -> None:
        self.types = TRAINING_TYPES
        self.current_type = None
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

    def get_serializer_class(self):
        if self.current_type == 'recognize':
            return RecognizeListSerializer
        if self.current_type == 'reproduce':
            return ReproduceListSerializer

        detail = f'type: {self.current_type} не подходи. Необходимо передать параметр type: {self.types}'
        raise Http404(detail)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        number_of_false_set = self.get_user().settings.number_of_false_set
        
        context.update({'number_of_false_set': number_of_false_set})
        return context

    def get_user(self):
        return cast(User, self.request.user)


class TrainingListUpdate(TrainingView, generics.ListAPIView, mixins.UpdateModelMixin):

    def get_object(self):
        data = self.request.POST.dict()
        pk = data['pk']

        try:
            obj = Dictionary.objects.get(id=pk)
        except:
            detail = f'Связь {pk} не найдена'
            raise Http404(detail)

        return obj
    
    def list(self, request, *args, **kwargs):
        user = self.get_user()
        self.current_type = self.get_type()
        queryset = Dictionary.objects.all(user.pk)[:2]

        serializer = self.get_serializer(queryset, **kwargs, many=True)

        if serializer.data:
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, *args, **kwargs):
        type = self.get_type()
        instance = self.get_object()
        user = self.get_user()

        levels = user.settings.levels

        is_correct = self.request.data['is_correct']  # type: ignore

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


class TrainingInfo(TrainingView):
    ...
#     def get(self, request, *args, **kwargs):
#         data = {}

#         # Проходимся по всем типам тренировок
#         for type in self.types:
#             filter = self.create_filte(type)
#             # Считаем количество тренировок для текущего типа
#             count_word_to_training_recognize = self.queryset.filter(
#                 **filter).count()

#             # Добавляем данные в словарь
#             data.update(
#                 {f'count_word_to_training_{type}': count_word_to_training_recognize}
#             )

#         return Response(status=status.HTTP_200_OK, data=data)
