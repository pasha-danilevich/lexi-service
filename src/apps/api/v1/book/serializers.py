from django.db import IntegrityError
from rest_framework import serializers
from apps.api.v1.book.services import get_start_end, get_user_bookmark
from apps.book.models import Book, Bookmark
from apps.book.utils import json_to_book
from apps.user.models import User
from config.settings import PAGE_SLICE_SIZE


from rest_framework import serializers
from apps.book.models import Book

# Общие поля для книги
common_book_fields = [
    'pk',
    'title',
    'author',
    'author_upload',
    'page_count',
    'slug',
]

class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = common_book_fields # Поля только для чтения

class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = common_book_fields + ['book', 'is_privet']  # Поля для создания
        extra_kwargs = {
            'book': {'write_only': True},
            'slug': {'read_only': True},
            'page_count': {'read_only': True},
        }
    
    def validate(self, attrs):
        print(attrs)
        book = attrs.get('book')
        user = self.context['request'].user
        
        # if isinstance(book, InMemoryUploadedFile):
        #     book = ... # достать текст
        
        if isinstance(book, str):
            if not book or len(book) == 0:
                data = {'book': ['Это поле не может быть пустым']}
                raise serializers.ValidationError({'book': ['Это поле не может быть пустым']})
            
            book = json_to_book(book)
            attrs['book'] = book

        attrs['page_count'] = len(book)
        attrs['author_upload'] = user

        return attrs
    
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({'details': 'Книга с таким названием и автором уже существует'})

class BookRetrieveSerializer(serializers.ModelSerializer):


    pages = serializers.SerializerMethodField()
    pages_slice = serializers.SerializerMethodField()
    bookmark = serializers.SerializerMethodField()
    slice_length = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = common_book_fields + [
            'pages_slice',
            'slice_length',
            'pages',
            'bookmark'
        ]
    
        
    def get_bookmark(self, obj):
        user: User = self.context['request'].user
        return get_user_bookmark(obj, user)

     
    def get_slice_length(self, obj):
        return PAGE_SLICE_SIZE

    def get_pages_slice(self, obj: Book):
        start, end = get_start_end(self.context, obj)
        return [start + 1, end]

    def get_pages(self, obj: Book):
        start, end = get_start_end(self.context, obj)
        pages_set = obj.book[start:end]
        return pages_set
    
