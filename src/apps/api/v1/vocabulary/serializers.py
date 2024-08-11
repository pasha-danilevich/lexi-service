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


class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = ['type_id', 'lvl'] # + ['time']

class DictionaryListSerializer(serializers.ModelSerializer):
    training = TrainingSerializer(many=True, read_only=True)
    word = WordSerializer(
        read_only=True,
        fields=['pk', 'text', 'transcription', 'form', 'part_of_speech']
    )
    is_many = serializers.SerializerMethodField()

    class Meta:
        model = Dictionary
        fields = ["pk", "word", "training", "is_many"] # + ["translation"]
    
    def get_is_many(self, obj: Dictionary):
        queryset = cast(
            models.QuerySet[Dictionary], 
            self.context.get('queryset', None)
        )
        
        return queryset.filter(word_id=obj.word).count() > 1  
        
    

    