from django.db import transaction
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.settings import api_settings

from djoser.serializers import UidAndTokenSerializer, UserCreateMixin, UserCreatePasswordRetypeSerializer

from apps.api.v1.book.serializers import BookSerializer
from apps.user.models import User, UserBookRelation, Settings
from apps.word.models import UserWord


User = get_user_model()


class CustomActivationSerializer(UidAndTokenSerializer):

    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs


class CustomUserCreateMixin(UserCreateMixin):
    def perform_create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            user.is_active = True
            user.save(update_fields=["is_active"])
            return user
    default_error_messages = {
        "password_mismatch": 'Поля для ввода пароля не совпадали.'
    }


class CustomUserCreatePasswordRetypeSerializer(CustomUserCreateMixin, UserCreatePasswordRetypeSerializer):
    pass


def _get_quantity(cls, field, value):
    return cls.objects.filter(**{field: value}).count()


def _get_list_words(queryset):
    word_list = []
    for user_word_relationship in queryset:
        word = user_word_relationship.word
        translation = word.translations.first()
        obj = {
            'text': word.text,
            'translation': translation.text
        }

        word_list.append(obj)
    return word_list


class ProfileSerializer(serializers.ModelSerializer):
    upload_book = serializers.SerializerMethodField()
    studied_word = serializers.SerializerMethodField()
    new_word = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'upload_book', 'studied_word', 'new_word']

    def get_upload_book(self, obj):
        return _get_quantity(UserBookRelation, 'user_id', obj.id)

    def get_studied_word(self, obj):
        return _get_quantity(UserWord, 'user_id', obj.id)

    def get_new_word(self, obj):
        user_words_queryset = obj.words.all()
        return _get_list_words(user_words_queryset)


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
            "book_id": book_data['pk']
        }
        return data


class SettingsSerializer(serializers.ModelSerializer):
    levels = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=3,
        max_length=30
    )

    theme = serializers.ChoiceField(choices=Settings.THEME_CHOICES, default='light')

    count_word_in_round = serializers.IntegerField(min_value=5, max_value=50)
    number_of_false_set = serializers.IntegerField(min_value=2, max_value=5)
    time_to_view_result = serializers.IntegerField(min_value=0, max_value=5000)

    class Meta:
        model = Settings
        fields = ['levels', 'theme', 'count_word_in_round', 'number_of_false_set', 'time_to_view_result']
        depth = 1

    def update(self, instance, validated_data):
        # Обновляем поля настроек
        instance.levels = validated_data.get('levels', instance.levels)
        instance.theme = validated_data.get('theme', instance.theme)
        instance.count_word_in_round = validated_data.get('count_word_in_round', instance.count_word_in_round)
        instance.number_of_false_set = validated_data.get('number_of_false_set', instance.number_of_false_set)
        instance.time_to_view_result = validated_data.get('time_to_view_result', instance.time_to_view_result)
        
        instance.save()
        return instance




class SettingsPageSerializer(serializers.ModelSerializer):
        
    settings = SettingsSerializer()
    class Meta:
        model = User
        fields = ['username', 'email', 'activated_email', 'settings']


    
