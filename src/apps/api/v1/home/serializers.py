from django.db.models import Q

from rest_framework import serializers

from apps.book.models import Book
from apps.word.models import Dictionary


class HomeSerializer(serializers.Serializer):
    learning_words = serializers.IntegerField()
    upload_books = serializers.IntegerField()
    new_words_today = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = self.context['request'].user
        self.initial_data = self.create_initial_data()

    def create_initial_data(self):

        dictionary = Dictionary.objects.all(self.user.id).order_by('-id')
        new_words_today = dictionary.get_new_words_today()
        upload_books = Book.objects.filter(author_upload=self.user.id)

        data = {
            'learning_words': dictionary.count(),
            'new_words_today': new_words_today.count(),
            'upload_books': upload_books.count()
        }

        return data
