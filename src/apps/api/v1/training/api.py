import inspect
from django.http import Http404
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .utils import get_false_set, get_time_on_lvl, is_last_level, is_first_level
from apps.word.utils import get_current_unix_time
from config.settings import print_local_var
from apps.api.v1.vocabulary.serializers import UserWord, UserWordSerializer, UserWordListSerializer


class Training(generics.GenericAPIView):
    queryset = UserWord.objects.all()
    serializer_class = UserWordListSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = None


class TrainingListUpdate(Training, generics.ListAPIView, mixins.UpdateModelMixin):

    def get_type(self):
        type = self.request.GET.get('type')
        if not type:
            detail = 'Необходимо передать параметр type: (recognize, reproduce)'
            raise Http404(detail)
        return type
    

    def list(self, request, *args, **kwargs):
        type = self.get_type()
        filter_field = type + '_time' + '__lte'
        
        filter = {
            filter_field: get_current_unix_time()
        }

        self.queryset = self.queryset.filter(**filter)
        queryset = self.filter_queryset(self.get_queryset())
        
        if type == 'recognize':
            
            number_of_false_set = self.request.user.settings["number_of_false_set"]
            kwargs = {
                "many": True, 
                "false_set": True, 
                "number_of_false_set": number_of_false_set
            }
        elif type == 'reproduce':
            kwargs = {"many": True}
            
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, **kwargs)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, **kwargs)
        return Response(serializer.data)

    def get_object(self):
        pk = self.request.data['pk']

        try:
            obj = UserWord.objects.get(id=pk)
        except:
            detail = f'Связь {pk} не найдена'
            raise Http404(detail)

        return obj

    def patch(self, request, *args, **kwargs):
        type = self.get_type()
        instance = self.get_object()
        user = self.request.user

        is_correct = self.request.data['is_correct']

        type_lvl = type + '_lvl'
        type_time = type + '_time'
        
        current_lvl = getattr(instance, type_lvl)
        instance_cuttent_time = getattr(instance, type_time)

        if is_correct and not is_last_level(user, current_lvl):
            new_lvl = current_lvl + 1
            
        elif not is_first_level(current_lvl):
            new_lvl = current_lvl - 1
        
        else:
            new_lvl = current_lvl

        new_time = instance_cuttent_time + get_time_on_lvl(user, new_lvl)

        setattr(instance, type_lvl, new_lvl)
        setattr(instance, type_time, new_time)

        instance.save(is_instance=True)

        return Response(status=status.HTTP_200_OK)
