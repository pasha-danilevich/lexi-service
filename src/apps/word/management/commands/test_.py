import logging
from cgitb import text
from typing import cast
import django
from django.core.management.base import BaseCommand
from apps.word.models import Dictionary, Word, Translation

from django.db.models import F, Value, BooleanField


django.setup()


# Настройка логирования
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        

        from django.db.models import Count, Case, When, BooleanField, Q

        result = (
            Dictionary.objects
            .filter(user_id=49)
            .annotate(word_count=Count('word_id'))
            .annotate(is_many=Case(
                When(word_count__gt=1, then=True),
                default=False,
                output_field=BooleanField()
            ))
            .values('word_id') 
        )

        
        result_list = list(result)

        for i in result_list:
            print(i)
            print('******')
        # serializer = DictionaryListSerializer(data=result_list, many=True)
        
        # if serializer.is_valid():
        #     data = serializer.data 
        #     for i in data:
        #         print(i)
        #         print('******')
        # else:
        #     print(serializer.errors)
            
        print('---------------')
        print(result.query)
        print('---------------')







from rest_framework import serializers


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['pk', 'text', 'transcription', 'form', 'part_of_speech']

class TranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = ['pk', 'text']

class DictionaryListSerializer(serializers.Serializer):
    # pk = serializers.IntegerField()
    word_id = serializers.IntegerField()
    # translation_id = serializers.IntegerField()
    is_many = serializers.BooleanField()
    word_count = serializers.IntegerField()

    word = WordSerializer(read_only=True)
    # translation = TranslationSerializer(read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Получаем объекты Word по их id
        word = Word.objects.get(pk=instance['word_id'])

        representation['word'] = WordSerializer(word).data


        return representation
