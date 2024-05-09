from django.test import TestCase

# Create your tests here.
from apps.word.models import Word


from config.settings import p
from django.test import TestCase


        
class TestStringMethods(TestCase):

    
    def test_get(self):
        word = Word.objects.create(
            text='hello',
            part='noun',
            transcription='hello',
            translation='привет'
        )
        queryset = Word.objects.all()
        
        lookup_field = 'text'
        lookup_value = 'helаlo'
        
        try:
            obj = queryset.get(**{lookup_field: lookup_value})
        except Word.DoesNotExist:
            print(f"Слово {lookup_value} не найдено.")
        print(obj)


