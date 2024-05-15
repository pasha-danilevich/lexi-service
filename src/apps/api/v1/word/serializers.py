from rest_framework import serializers
from apps.word.models import Word, Translation, Synonym, Meaning

class TranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = ['text', 'part_of_speech', 'gender', 'frequency']

class SynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Synonym
        fields = ['text', 'part_of_speech', 'gender', 'frequency']

class MeaningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meaning
        fields = ['text']

class WordSerializer(serializers.ModelSerializer):
    translations = TranslationSerializer(many=True, read_only=True)
    synonyms = SynonymSerializer(many=True, read_only=True)
    meanings = MeaningSerializer(many=True, read_only=True)

    class Meta:
        model = Word
        fields = ['text', 'part_of_speech', 'transcription', 'translations', 'synonyms', 'meanings']
