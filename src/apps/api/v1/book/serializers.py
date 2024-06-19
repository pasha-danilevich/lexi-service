from rest_framework import serializers
from apps.book.models import Book
from apps.user.models import UserBookRelation


def bookmark(self, obj):
    if self.user:  
        bookmark = UserBookRelation.objects.filter(user_id=self.user.id, book=obj.pk).first()
        if bookmark:
            data = {
                'pk': bookmark.pk,
                'target_page': bookmark.target_page
            }
            return data
    else:
        return None

class BookSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    bookmark = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = [
            'pk',
            'title',
            'author',
            'author_upload',
            'page_count',
            'slug',
            'book',
            'bookmark'
        ]
        extra_kwargs = {
            'slug': {'read_only': True},
            'author_upload': {'write_only': True},
            'book': {'write_only': True}
        }
        
    def get_bookmark(self, obj):
        return bookmark(self=self, obj=obj)


class BookRetrieveSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        self.page = kwargs.pop('page')
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    pages = serializers.SerializerMethodField()
    bookmark = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'pk',
            'title',
            'author',
            'author_upload',
            'page_count',
            'slug',
            'pages',
            'bookmark'
        ]

    def get_pages(self, obj):
        page = self.page - 1
        size_page_slice = 50

        start = (page // size_page_slice) * size_page_slice
        end = (page // size_page_slice) * size_page_slice + size_page_slice

        pages_set = obj.book[start:end]
        return pages_set
    
    def get_bookmark(self, obj):
        return bookmark(self=self, obj=obj)
        
