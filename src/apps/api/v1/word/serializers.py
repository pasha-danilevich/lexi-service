from rest_framework import serializers
from apps.word.models import Word

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = [
            'pk', 
            'text', 
            'path', 
            'transcription', 
            'translation'
            ]