from rest_framework import serializers
from apps.word.models import Dictionary, Training


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
        fields = ['type_id', 'lvl', 'time']

class DictionaryListSerializer(serializers.ModelSerializer):
    training = TrainingSerializer(many=True, read_only=True)

    class Meta:
        model = Dictionary
        fields = ["pk", "word", "translation", "training"]
        depth = 1
    

    