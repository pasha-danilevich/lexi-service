from rest_framework import serializers
from django.db.models import Q

from apps.book.models import Book
from apps.word.models import UserWord
from .utils import get_list_words, get_beginning_day, get_ending_day, get_new_words_today

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
        
        user_words = UserWord.objects.filter(user_id = self.user.id)
        
        beginning_day = get_beginning_day()
        ending_day = get_ending_day()
    
        new_words_today = get_new_words_today(user_words, beginning_day, ending_day)
        
        
        data = {
            'learning_words': user_words.all().count(),
            'new_words_today': new_words_today.count(),
            'upload_books': Book.objects.filter(author_upload=self.user.id).count(),
            'recently_added_words': get_list_words(queryset=user_words[:5])
        }
        return data
        
            

