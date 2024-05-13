from django.test import TestCase

from apps.user.models import User
from apps.word.utils import get_current_unix_time

# Create your tests here.
from .models import  Word, UserWord


from config.settings import p
from django.test import TestCase


       
class TestStringMethods(TestCase):
    
    
    def test_get(self):
        
        queryset = Word.objects.all()
        
        lookup_field = 'text'
        lookup_value = 'helаlo'
        
        try:
            obj = queryset.get(**{lookup_field: lookup_value})
            ...
        except Word.DoesNotExist:
            ...
            
    def test_create_word(self):
        request_word = 'bird'
        data = {
            "text": 'bird',
            "part": 'noun',
            "transcription": 'bird',
            "translation": 'птица',
            "synonym": ["птичка","пташка","перелетная птица"]
        }
        word, created = Word.objects.get_or_create(
            text=request_word,
            defaults={**data}
        )     


    # def test_create_userword(self):
        
    #     user_word_relation = UserWord.objects.create(
    #         user=user, 
    #         word=word
    #         ) 
        
    # def test_get_related_word(self):
        
        
        
    # def test_create_traing(self):
    #     training = Training.objects.create()
    #     print(training.__dict__)


