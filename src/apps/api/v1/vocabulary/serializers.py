from typing import cast
from rest_framework import serializers
from apps.api.v1.word.serializers import WordSerializer

from apps.word.models import Dictionary, Training
from django.db import models


class DictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictionary
        fields = [
            "pk",
            "user",
            "word",
            "translation"
        ]
        extra_kwargs = {
            'user': {'write_only': True},
            'word': {'write_only': True},
            'translation': {'write_only': True},
        }



class DictionaryListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    date_added = serializers.DateTimeField()
    word_id = serializers.IntegerField()
    word_form = serializers.CharField()
    word_transcription = serializers.CharField()
    word_text = serializers.CharField()
    part_of_speech = serializers.CharField()
    lvl_sum = serializers.FloatField()
    is_many = serializers.BooleanField()
