from rest_framework import serializers
from django.db.models import Q

from apps.book.models import Book
from apps.word.models import Dictionary
from .services import get_list_words, get_new_words_today

from django.utils.timezone import localtime



class HomeSerializer(serializers.Serializer):
    learning_words = serializers.IntegerField()
    upload_books = serializers.IntegerField()
    new_words_today = serializers.IntegerField()
    recently_added_words = serializers.ListField(child=serializers.CharField())
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = self.context['request'].user
        self.initial_data = self.create_initial_data()
        
    def create_initial_data(self):
        
        dictionary = Dictionary.objects.filter(user_id = self.user.id).order_by('-id')
        upload_books = Book.objects.filter(author_upload=self.user.id)
    
        new_words_today = get_new_words_today(dictionary)
        
        
        data = {
            'learning_words': dictionary.all().count(),
            'new_words_today': new_words_today.count(),
            'upload_books': upload_books.count(),
            'recently_added_words': get_list_words(dictionary=dictionary[:5])
        }
        return data
        
            

