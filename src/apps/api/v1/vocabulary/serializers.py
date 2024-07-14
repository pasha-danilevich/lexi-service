from rest_framework import serializers
from apps.api.v1.training.utils import get_false_set
from apps.word.models import Dictionary
from apps.api.v1.word.serializers import WordSerializer


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


class DictionaryListSerializer(serializers.ModelSerializer):
    
    word = serializers.SerializerMethodField()
    
    class Meta:
        model = Dictionary
        fields = ["pk", "word"]
        
    
    def get_word(self, obj):
        word = obj.word
        fields = ('pk', 'text', 'part_of_speech', 'transcription')
        serializers = WordSerializer(word, fields=fields)
        data = serializers.data
        return data
    