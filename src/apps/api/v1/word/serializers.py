from rest_framework import serializers
from apps.word.models import Word

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['pk', 'text', 'part', 'transcription', 'translation', 'synonym']
        extra_kwargs = {field: {'write_only': True} for field in fields}
        extra_kwargs.update({'pk': {'read_only': True}}) 