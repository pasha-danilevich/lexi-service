from django.db import IntegrityError
from django.core.files.uploadedfile import InMemoryUploadedFile

from rest_framework import serializers

from apps.api.v1.book import text_extractor
from apps.api.v1.book.services import get_start_end, get_user_bookmark
from apps.api.v1.book.text_extractor import TextExtractor
from apps.book.models import Book
from apps.book.utils import json_to_book
from apps.user.models import User
from rest_framework.exceptions import ValidationError

from config.settings import PAGE_SLICE_SIZE

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
        fields = common_book_fields  # Поля только для чтения

from rest_framework import serializers
from django.core.files.uploadedfile import InMemoryUploadedFile

class BaseBookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = common_book_fields + ['is_privet']
        extra_kwargs = {
            'slug': {'read_only': True},
            'page_count': {'read_only': True},
        }


    def validate(self, attrs):
        print(attrs, self.__class__.__name__)
        book = attrs['book']
        attrs['author_upload'] = self.context['request'].user
        attrs['page_count'] = len(book)
        return super().validate(attrs)

    # TODO
    # save отлавить ошибки уникальности и дургие ошибки
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            # Обработка ошибки уникальности
            raise ValidationError({'details': 'Запись с такими данными уже существует.'})
        except Exception as e:
            # Обработка других ошибок
            raise ValidationError({'details': f'Произошла ошибка: {str(e)}'})


class FileBookCreateSerializer(BaseBookCreateSerializer):
    book = serializers.FileField(write_only=True)

    class Meta(BaseBookCreateSerializer.Meta):
        fields = BaseBookCreateSerializer.Meta.fields + ['book']
        
    def validate_book(self, value):
        if isinstance(value, InMemoryUploadedFile):
            text_extractor = TextExtractor(uploaded_file=value)
            value = text_extractor.extract_text()  
        return json_to_book(value)


class JsonBookCreateSerializer(BaseBookCreateSerializer):
    book = serializers.JSONField(write_only=True)

    class Meta(BaseBookCreateSerializer.Meta):
        fields = BaseBookCreateSerializer.Meta.fields + ['book']

    def validate_book(self, value):
        return json_to_book(value)
    
    
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
