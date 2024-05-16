from rest_framework import serializers
from apps.word.models import Word, Translation, Synonym, Meaning

class TranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = ['pk', 'text', 'part_of_speech', 'gender', 'frequency']

class SynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Synonym
        fields = ['pk', 'text', 'part_of_speech', 'gender', 'frequency']

class MeaningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meaning
        fields = ['text']

class WordSerializer(serializers.ModelSerializer):
    
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)  # Извлекаем аргумент 'fields' из kwargs
        super(WordSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
    
    translations = TranslationSerializer(many=True, read_only=True)
    synonyms = SynonymSerializer(many=True, read_only=True)
    meanings = MeaningSerializer(many=True, read_only=True)

    class Meta:
        model = Word
        fields = ['pk', 'text', 'part_of_speech', 'transcription', 'translations', 'synonyms', 'meanings']
