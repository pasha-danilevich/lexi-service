from rest_framework import serializers
from apps.book.models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'pk', 
            'title', 
            'author', 
            'author_upload', 
            'page_count', 
            'slug', 
            'book'
            ]
        extra_kwargs = {
            'slug': {'read_only': True},
            'author_upload': {'write_only': True}
            }