from rest_framework import serializers
from apps.api.v1.training.utils import get_false_set
from apps.word.models import UserWord
from apps.api.v1.word.serializers import WordSerializer


class UserWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWord
        fields = [
            "pk",
            "user",
            "word"
        ]
        extra_kwargs = {
            'user': {'write_only': True},
            'word': {'write_only': True}
        }


class UserWordListSerializer(serializers.ModelSerializer):
    
    word = serializers.SerializerMethodField()
    false_set = serializers.SerializerMethodField()
    
    class Meta:
        model = UserWord
        fields = ["pk", "word", "false_set", "recognize_lvl", "reproduce_lvl"]
        
    def __init__(self, *args, **kwargs):
        self.include_false_set = kwargs.pop('false_set', False)
        self.number_of_false_set = kwargs.pop('number_of_false_set', False)
        super(UserWordListSerializer, self).__init__(*args, **kwargs)
    
    def get_word(self, obj):
        word = obj.word
        fields = ('pk', 'text', 'part_of_speech', 'transcription')
        serializers = WordSerializer(word, fields=fields)
        data = serializers.data
        data.update({'translation': word.translations.first().text})
        return data
    
    def get_false_set(self, obj):
        if self.include_false_set:
            word = obj.word
            
            kwargs = {
                "instance": word,
                "part_of_speech": word.part_of_speech,
                "number_of_false_set": self.number_of_false_set
            }
            
            return get_false_set(**kwargs)
        return None