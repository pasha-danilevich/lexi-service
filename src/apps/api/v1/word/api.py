from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from apps.api.v1.word.serializers import WordSerializer, Word

class WordCreate(generics.GenericAPIView, mixins.CreateModelMixin):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    lookup_field = 'text'
    
    def get_object(self, lookup_value: str):
        try:
            instance = self.queryset.get(**{self.lookup_field: lookup_value})
            return instance
        except Word.DoesNotExist:
            return None
        
    
    def post(self, request, *args, **kwargs):
        lookup_value = self.request.data['text']
        instance = self.get_object(lookup_value)
        
        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return super().create(request, *args, **kwargs)

