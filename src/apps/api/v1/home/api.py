from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.word.models import Dictionary

from .serializers import HomeSerializer



class HomeView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated] 
    serializer_class = HomeSerializer
    
    
    def get(self, request):
        serializer = self.get_serializer()
        serializer.is_valid()
        
        return Response(serializer.data)
    
