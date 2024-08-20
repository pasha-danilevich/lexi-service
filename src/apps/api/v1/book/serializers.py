from rest_framework import serializers
from apps.api.v1.book.services import get_start_end, get_user_bookmark
from apps.book.models import Book, Bookmark
from apps.user.models import User
from config.settings import PAGE_SLICE_SIZE


common_book_fields = [
    'pk',
    'title',
    'author',
    'author_upload',
    'page_count',
    'slug',
]


class BookListCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = common_book_fields + ['book', 'is_privet']
        extra_kwargs = {
            'slug': {'read_only': True},
            'author_upload': {'write_only': True},
            'book': {'write_only': True},
            'is_privet': {'write_only': True},
        }



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
    
