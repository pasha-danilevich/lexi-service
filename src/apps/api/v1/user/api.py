from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.user.models import UserBookRelation
from apps.api.v1.user.serializers import BookmarkSerliazer

from djoser.views import UserViewSet
from djoser import signals
from djoser.conf import settings
from djoser.compat import get_user_email
from rest_framework.decorators import action


class BookmarkList(generics.ListAPIView):
    

    serializer_class = BookmarkSerliazer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        
        queryset = UserBookRelation.objects.filter(user_id = request.user.id)
        serializer = BookmarkSerliazer(queryset, many=True)
        return Response(serializer.data)
    
class UserActivate(UserViewSet):
    
    @action(["post"], detail=False)
    def activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.activated_email = True
        user.save()

        signals.user_activated.send(
            sender=self.__class__, user=user, request=self.request
        )

        if settings.SEND_CONFIRMATION_EMAIL:
            context = {"user": user}
            to = [get_user_email(user)]
            settings.EMAIL.confirmation(self.request, context).send(to)

        return Response(status=status.HTTP_204_NO_CONTENT)