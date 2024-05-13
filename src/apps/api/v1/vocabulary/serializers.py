from rest_framework import serializers
from apps.word.models import UserWord
from apps.api.v1.word.serializers import WordSerializer

fields = [
    "user",
    "word",
    "recognize_lvl",
    "recognize_time",
    "reproduce_lvl",
    "reproduce_time"
]

class UserWordSerializer(serializers.ModelSerializer):
    word_view = serializers.SerializerMethodField()
    class Meta:
        model = UserWord
        fields = [
            "pk",
            "user",
            "word",
            "word_view",
            "recognize_lvl",
            "recognize_time",
            "reproduce_lvl",
            "reproduce_time"
        ] 
        extra_kwargs = {
            'user': {'write_only': True},
            'word': {'write_only': True},
            'word_view': {'read_only': True},
            'recognize_lvl': {'read_only': True},
            'recognize_time': {'read_only': True}, 
            'reproduce_lvl': {'read_only': True}, 
            'reproduce_time': {'read_only': True}     
        }
    
    def get_word_view(self, obj):
        word_obj = obj.word
        serializers = WordSerializer(word_obj)
        return serializers.data