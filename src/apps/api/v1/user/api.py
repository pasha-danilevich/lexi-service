from rest_framework import generics
from rest_framework.response import Response

from apps.word.models import Word, UserWordRelation
from apps.user.models import User, UserBookRelation
from apps.api.v1.user.serializers import ProfileSerializer


class RetrieveUser(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'username'
    

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serialize = self.get_serializer(instance)
        data = serialize.data
        return Response(data) 
    
    