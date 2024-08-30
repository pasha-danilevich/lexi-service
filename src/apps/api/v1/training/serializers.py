from rest_framework import serializers

from apps.api.v1.training.false_set import FalseSet
from apps.word.models import Training


class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = ["pk", "lvl"]


class BaseTrainingListSerializer(serializers.Serializer):
    word_text = serializers.CharField(source='word__text')
    word_transcription = serializers.CharField(source='word__transcription')
    translation_text = serializers.CharField(source='translation__text')
    part_of_speech_text = serializers.CharField(
        source='word__part_of_speech__text')
    training_id = serializers.IntegerField(source='training__id')
    training_lvl = serializers.IntegerField(source='training__lvl')

    class Meta:
        fields = [
            "word_text",
            "word_transcription",
            "translation_text",
            "part_of_speech_text",
            "training_id",
            "training_lvl"
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        new_representation = {
            "word": {
                "text": representation["word_text"],
                "translation": representation["translation_text"],
                "transcription": representation["word_transcription"],
                "part_of_speech": representation["part_of_speech_text"],
            },
            "training": {
                "pk": representation["training_id"],
                "lvl": representation["training_lvl"],
            }
        }
        false_set = representation.get("false_set", None)
        if false_set:
            new_representation.update(
                {"false_set": representation["false_set"]})

        return new_representation


class ReproduceListSerializer(BaseTrainingListSerializer):

    class Meta(BaseTrainingListSerializer.Meta):
        fields = BaseTrainingListSerializer.Meta.fields


class RecognizeListSerializer(BaseTrainingListSerializer):
    false_set = serializers.SerializerMethodField()

    class Meta(BaseTrainingListSerializer.Meta):
        fields = BaseTrainingListSerializer.Meta.fields + ["false_set"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.false_set_obj = FalseSet(
            queryset=args[0],
            word_count=self.context.get('number_of_false_set', 2)
        )

    def get_false_set(self, obj: dict):

        word_pos = obj['word__part_of_speech__text']
        false_set_list = self.false_set_obj.get_list_false_set_word(
            pos=word_pos
        )

        return false_set_list

