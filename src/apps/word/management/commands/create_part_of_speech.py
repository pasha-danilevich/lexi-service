import logging
from cgitb import text
from typing import cast
import django
from django.core.management.base import BaseCommand
from apps.word.models import PartOfSpeech, Synonym, Translation, Word
from django.db.models import QuerySet

django.setup()


# Настройка логирования
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        self.update_words()
        # self.set_null_to_part_of_speech()

    def update_words(self):
        import time
        start_time = time.time()  # Запоминаем время начала выполнения

        words_to_update = Synonym.objects.all()
        part_of_speech_map = {}

        for word in words_to_update:
            part_of_speech_name = word.part_of_speech_name

            if part_of_speech_name:
                part_of_speech, created = PartOfSpeech.objects.get_or_create(
                    text=part_of_speech_name
                )
                part_of_speech_map[word.pk] = part_of_speech

        for word in words_to_update:
            if word.pk in part_of_speech_map:
                word.part_of_speech = part_of_speech_map[word.pk]

        Synonym.objects.bulk_update(words_to_update, ['part_of_speech'])

        end_time = time.time()  # Запоминаем время окончания выполнения
        execution_time = end_time - start_time  # Вычисляем время выполнения
        logging.info(
            f'Время выполнения функции update_words: {execution_time:.2f} секунд')

    def set_null_to_part_of_speech(self):
        import time
        start_time = time.time()

        words_to_update = Word.objects.all()

        for word in words_to_update:
            word.part_of_speech = None # type: ignore
            word.save()
 
        end_time = time.time()  # Запоминаем время окончания выполнения
        execution_time = end_time - start_time  # Вычисляем время выполнения
        logging.info(
            f'Время выполнения функции set_null_to_part_of_speech: {execution_time:.2f} секунд')
