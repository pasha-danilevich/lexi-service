from django.db import transaction
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.settings import api_settings

from djoser.serializers import UidAndTokenSerializer, UserCreateMixin, UserCreatePasswordRetypeSerializer

from apps.book.models import UserBook
from apps.user.models import User, Settings
from apps.word.models import Dictionary


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




class SettingsSerializer(serializers.ModelSerializer):
    levels = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=3,
        max_length=30
    )

    theme = serializers.ChoiceField(choices=Settings.THEME_CHOICES, default='light')

    count_word_in_round = serializers.IntegerField(min_value=5, max_value=25)
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


    
