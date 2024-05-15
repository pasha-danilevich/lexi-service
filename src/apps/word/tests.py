import pprint
from django.test import TestCase

from apps.api.v1.word.utils import get_or_create_word, word_list_create
from apps.api.v1.word.yandex_dictionary import fetch_word_data
from apps.user.models import User
from apps.word.utils import get_current_unix_time

# Create your tests here.
from apps.word.models import Word, Translation, Synonym, Meaning, UserWord


from config.settings import p, print_local_var
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
        
            
                    
        request_word = 'get'
        word_set = fetch_word_data(request_word)
        
        
            
        word1 = get_or_create_word(word_set, request_word)
        word = get_or_create_word(word_set, request_word)
        print(word)
        print(word.translations.all())
        print(word.synonyms.all())
        print(word.meanings.all())
            
    # def test_create_userword(self):

    #     user_word_relation = UserWord.objects.create(
    #         user=user,
    #         word=word
    #         )

    # def test_get_related_word(self):

    # def test_create_traing(self):
    #     training = Training.objects.create()
    #     print(training.__dict__)
