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
            'author_upload': {'write_only': True},
            'book': {'write_only': True}
        }


class BookRetrieveSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        self.page = kwargs.pop('page')
        super().__init__(*args, **kwargs)

    pages = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'pk',
            'title',
            'author',
            'author_upload',
            'page_count',
            'slug',
            'pages'
        ]

    def get_pages(self, obj):
        page = self.page
        size_page_slice = 10

        start = (page // size_page_slice) * size_page_slice
        end = (page // size_page_slice) * size_page_slice + size_page_slice

        pages_set = obj.book[start:end]
        return pages_set
