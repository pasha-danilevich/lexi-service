from rest_framework import serializers
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
    class Meta:
        model = UserWord
        fields = ["word", "recognize_lvl", "reproduce_lvl"]
        
    def get_word(self, obj):
        word = obj.word
        fields = ('pk', 'text', 'part_of_speech', 'transcription')
        serializers = WordSerializer(word, fields=fields)
        data = serializers.data
        data.update({'translation': word.translations.first().text})
        return data