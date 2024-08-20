from typing import cast
from rest_framework import serializers
from apps.api.v1.book.serializers import BookListCreateSerializer
from apps.book.models import Bookmark


class BookmarkListSerializer(serializers.ModelSerializer):

    book_cover = serializers.SerializerMethodField()

    class Meta:
        model = Bookmark
        fields = ['pk', 'book_cover', 'target_page']
        extra_kwargs = {'book_cover': {'read_only': True}}

    def get_book_cover(self, obj):
        serializer = BookListCreateSerializer(obj.book)
        book_data = cast(dict, serializer.data)
        data = {
            "title": book_data['title'],
            "author": book_data['author'],
            "slug": book_data['slug'],
            "book_id": book_data['pk']
        }
        return data
