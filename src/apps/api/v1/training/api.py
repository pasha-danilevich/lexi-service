from typing import Any, cast
from django.http import Http404
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .permissions import IsOwnerOrReadOnly
from apps.api.v1.training.serializers import RecognizeListSerializer, ReproduceListSerializer
from apps.user.models import User

from .services import get_new_lvl, get_new_time

from apps.word.models import Dictionary, Training


from config.settings import TRAINING_TYPES, TRAINING_TYPES_ID


class TrainingView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
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

        context.update({
            'number_of_false_set': number_of_false_set,
            'type_id': TRAINING_TYPES_ID[self.get_type()]
        })

        return context

    def get_user(self):
        return cast(User, self.request.user)


class TrainingListUpdate(TrainingView, generics.ListAPIView, mixins.UpdateModelMixin):

    def get_training(self) -> Training:
        data = self.request.data  # type: ignore
        pk = data['pk']

        try:
            obj = Training.objects.get(id=pk)

            self.check_object_permissions(self.request, obj)
            return obj
        except Training.DoesNotExist:
            details = f'Связь {pk} не найдена'
            raise Http404(details)

    def list(self, request, *args, **kwargs):
        user = self.get_user()
        self.current_type = self.get_type()
        type_id = TRAINING_TYPES_ID[self.current_type]
        
        results = Dictionary.objects.all(
            user.pk
        ).current(
            type_id
        ).select_related(
            'word', 'translation', 'word__part_of_speech'
        ).values(
            'word__text',
            'word__transcription',
            'translation__text',
            'word__part_of_speech__text',
            'training__id',
            'training__lvl'
        )[:user.settings.count_word_in_round]
        
        serializer = self.get_serializer(results, **kwargs, many=True)
        
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, *args, **kwargs):
        training = self.get_training()
        user = self.get_user()
        levels = user.settings.levels
        data = self.request.data  # type: ignore

        new_lvl = get_new_lvl(
            is_correct=data['is_correct'],
            levels=levels,
            current_lvl=training.lvl
        )

        training.lvl = new_lvl
        training.time = get_new_time(levels, new_lvl)

        training.save()

        return Response(status=status.HTTP_200_OK)


class TrainingInfo(TrainingView):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        data = {}
        queryset = Dictionary.objects.all(user_id=user.pk)
        for type in self.types:
            word_to_training = queryset.current(
                type_id=TRAINING_TYPES_ID[type])

            data.update(
                {f'count_word_to_training_{type}': word_to_training.count()}
            )

        return Response(status=status.HTTP_200_OK, data=data)
