from rest_framework import serializers
from rest_framework.settings import api_settings

from django.db import transaction
from django.contrib.auth import get_user_model


from apps.api.v1.book.serializers import BookSerializer
from apps.user.models import User, UserBookRelation
from apps.word.models import UserWord, Word

from djoser.serializers import UserCreateMixin, UserCreatePasswordRetypeSerializer




User = get_user_model()

class CustomUserCreateMixin(UserCreateMixin):
    def perform_create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            user.is_active = True
            user.save(update_fields=["is_active"])
            return user

class CustomUserCreatePasswordRetypeSerializer(CustomUserCreateMixin, UserCreatePasswordRetypeSerializer):
    pass

def _get_quantity(cls, field, value):
    return cls.objects.filter(**{field: value}).count()

def _get_list_words(queryset):
    return [{
        "text": Word.objects.get(id=word.word_id).text, 
        "translation": Word.objects.get(id=word.word_id).translation
        }
        for word in queryset
    ]

class ProfileSerializer(serializers.ModelSerializer):
    upload_book = serializers.SerializerMethodField()
    studied_word = serializers.SerializerMethodField()
    new_word = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'upload_book', 'studied_word', 'new_word', 'settings']

    def get_upload_book(self, obj):
        return _get_quantity(UserBookRelation, 'user_id', obj.id)

    def get_studied_word(self, obj):
        return _get_quantity(UserWord, 'user_id', obj.id)

    def get_new_word(self, obj):
        queryset_new_word = UserWord.objects.filter(user_id=obj.id)[:7]
        return _get_list_words(queryset_new_word)
    
class BookmarkSerializer(serializers.ModelSerializer):

    book_cover = serializers.SerializerMethodField()
    
    class Meta:
        model = UserBookRelation
        fields = ['pk', 'book_cover', 'target_page']
        extra_kwargs = {'book_cover': {'read_only': True}}
        
    def get_book_cover(self, obj):
        book_serializer = BookSerializer(obj.book)
        book_data = book_serializer.data
        data = {
            "title": book_data['title'],
            "author": book_data['author'],
            "slug": book_data['slug'],
        }
        return data


