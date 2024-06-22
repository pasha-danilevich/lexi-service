from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.user.models import UserBookRelation
from apps.word.models import UserWord

from .serializers import HomeSerializer



class HomeView(generics.GenericAPIView):
    queryset = UserWord.objects.all().order_by('-id')
    permission_classes = (IsAuthenticated, )
    
    def get_queryset(self):
        queryset = self.queryset.filter(user_id = self.request.user.id)
        return queryset
    
    
    def get(self, request):
        queryset = self.get_queryset()
        user = self.request.user
        
        serializer = HomeSerializer(queryset=queryset, user = user)
        serializer.is_valid()
        
        return Response(serializer.data)
    
