import time
import requests
import json
from django.core.management.base import BaseCommand

from apps.word.models import Translation, Word


def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Функция {func.__name__} выполнялась {end_time - start_time:.6f} секунд.")
        return result
    return wrapper

class Command(BaseCommand):
    help = 'Заполняет базу данных случайными словами и их переводами'

    def handle(self, *args, **options):
        for _ in range(1000):
            self.populate() 

    @measure_time
    def populate(self):
        random_word, random_translation = self.get_random_word_translation()

        if random_word and random_translation:
            response = self.post_word(random_word, random_translation)
            print(response.text)

    def get_random_word_translation(self):
        random_word = Word.objects.order_by('?').first()
        if not random_word:
            return None, None

        word_translations = random_word.translations.all()
        random_translation = word_translations.order_by('?').first()

        if not random_translation:
            return random_word, None

        return random_word, random_translation

    def post_word(self, word: Word, translation: Translation):
        url = "http://127.0.0.1:8000/api/vocabulary/"

        payload = json.dumps({
            "word": word.pk,
            "translation": translation.pk
        })

        headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI0Nzg0MTY4LCJpYXQiOjE3MjQxNzkzNjgsImp0aSI6IjQ2YjMzZDM0ZWI0ODQxZDc4ZTY0ZWVkNGI1N2YxZDhmIiwidXNlcl9pZCI6NDl9.zNVkdsALduxTHot2h_xC2pxVOUigYJgWrrba-2wWDxY',
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, data=payload)

        return response