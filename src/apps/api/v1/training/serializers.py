from typing import cast
from rest_framework import serializers
from apps.api.v1.training.utils import get_false_set
from apps.word.models import Dictionary, Word
from apps.api.v1.word.serializers import WordSerializer

class BaseTrainingListSerializer(serializers.ModelSerializer):
    word = serializers.SerializerMethodField()
    lvl = serializers.SerializerMethodField()

    class Meta:
        model = Dictionary
        fields = ["pk", "word", "lvl"]

    def get_word(self, obj: Dictionary):
        word = cast(Word, obj.word)
        fields = ('pk', 'text', 'part_of_speech', 'transcription')
        serializers = WordSerializer(word, fields=fields)
        data = serializers.data
        data.update({'translation': word.translations.first().text}) # type: ignore
        return data

    def get_lvl(self, obj: Dictionary):
        print(obj.training)
        return None

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


# class TrainingWordListSerializer(serializers.ModelSerializer):
    
#     word = serializers.SerializerMethodField()
#     false_set = serializers.SerializerMethodField()
    
#     class Meta:
#         model = Dictionary
#         fields = ["pk", "word", "false_set", "recognize_lvl", "reproduce_lvl"]
        
#     def __init__(self, *args, **kwargs):
#         self.include_false_set = kwargs.pop('false_set', False)
#         self.number_of_false_set = kwargs.pop('number_of_false_set', False)
#         super(TrainingWordListSerializer, self).__init__(*args, **kwargs)
    
#     def get_word(self, obj):
#         word = obj.word
#         fields = ('pk', 'text', 'part_of_speech', 'transcription')
#         serializers = WordSerializer(word, fields=fields)
#         data = serializers.data
#         data.update({'translation': word.translations.first().text}) # type: ignore
#         return data
    
#     def get_false_set(self, obj):
#         if self.include_false_set:
#             word = obj.word
            
#             kwargs = {
#                 "instance": word,
#                 "part_of_speech": word.part_of_speech,
#                 "number_of_false_set": self.number_of_false_set
#             }
            
#             return get_false_set(**kwargs)
#         return None