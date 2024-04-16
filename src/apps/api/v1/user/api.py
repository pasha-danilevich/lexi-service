from rest_framework import generics
from rest_framework.response import Response

from apps.word.models import Word, UserWordRelation
from apps.user.models import User, UserBookRelation
from apps.api.v1.user.serializers import UserSerializer

def get_quantity(cls, field, value):
    return cls.objects.filter(**{field: value}).count()

class RetrieveUser(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        upload_book = get_quantity(
            cls=UserBookRelation, 
            field='user_id', 
            value=instance.id
            )
        studied_word = get_quantity(
            cls=UserWordRelation, 
            field='user_id',
            value=instance.id
            )
        queryset_new_word = UserWordRelation.objects.filter(user_id=instance.id)[:7]
        new_words = [{
            "text": Word.objects.get(id=word.word_id).text, 
            "translation": Word.objects.get(id=word.word_id).translation
            }
            for word in queryset_new_word
        ]
        data = {
            "username": instance.username,
            "upload-book": upload_book,
            "studied-word": studied_word,
            "new-word": new_words
        }
        

        return Response(data) 
    
    