from typing import cast
from rest_framework import serializers
from apps.api.v1.training.services import get_false_set
from apps.word.models import Dictionary, Training, Word
from apps.api.v1.word.serializers import WordSerializer

class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = ["pk", "lvl"]
        
class BaseTrainingListSerializer(serializers.ModelSerializer):
    word = serializers.SerializerMethodField()
    training = serializers.SerializerMethodField()

    class Meta:
        model = Dictionary
        fields = ["pk", "word", "training"]

    def get_word(self, obj: Dictionary):
        word = cast(Word, obj.word)
        fields = ('pk', 'text', 'part_of_speech', 'transcription')
        serializers = WordSerializer(word, fields=fields)
        data = serializers.data
        data.update({'translation': word.translations.first().text}) # type: ignore
        return data

    def get_training(self, obj):
        training = obj.training.get(type_id=self.context['type_id'])
        serializers = TrainingSerializer(training)
        data = serializers.data
        
        return data


class ReproduceListSerializer(BaseTrainingListSerializer):

    class Meta(BaseTrainingListSerializer.Meta):
        fields = BaseTrainingListSerializer.Meta.fields


class RecognizeListSerializer(BaseTrainingListSerializer):
    false_set = serializers.SerializerMethodField()

    class Meta(BaseTrainingListSerializer.Meta):
        fields = BaseTrainingListSerializer.Meta.fields + ["false_set"]

    def get_false_set(self, obj: Dictionary):
        word = cast(Word, obj.word)

        kwargs = {
            "instance": word,
            "part_of_speech": word.part_of_speech,
            "number_of_false_set": self.context.get('number_of_false_set', False)
        }

        return get_false_set(**kwargs)
