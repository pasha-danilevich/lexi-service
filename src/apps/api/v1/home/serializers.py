from rest_framework import serializers
from django.db.models import Q

from apps.book.models import Book
from .utils import get_beginning_day, get_ending_day
from apps.word.utils import get_current_unix_time

class HomeSerializer(serializers.Serializer):
    learning_words = serializers.IntegerField()
    upload_books = serializers.IntegerField()
    count_reproduce_to_learn = serializers.IntegerField()
    count_recognize_to_learn = serializers.IntegerField()
    new_words_today = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop('queryset', None)
        user = kwargs.pop('user', None)
        # now = kwargs.pop('now', None)

        super().__init__(*args, **kwargs)

        if queryset is not None:
            beginning_day = get_beginning_day()
            ending_day = get_ending_day()
            now = get_current_unix_time()
            
            reproduce_queryset_words_to_learning = queryset.filter(
                reproduce_time__lte=now
            )
            recognize_queryset_words_today = queryset.filter(
                recognize_time__lte=now
            )
            new_words_today = queryset.filter(
                Q(recognize_time__gte=beginning_day) & Q(recognize_time__lte=ending_day)
            )
            
            
            data = {
                'learning_words': queryset.all().count(),
                'count_reproduce_to_learn': reproduce_queryset_words_to_learning.count(),
                'count_recognize_to_learn': recognize_queryset_words_today.count(),
                'new_words_today': new_words_today.count(),
                'upload_books': Book.objects.filter(author_upload=user.id).count()
            }
            
            self.initial_data = data

            

