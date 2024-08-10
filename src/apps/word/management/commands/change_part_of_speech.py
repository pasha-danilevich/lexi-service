from typing import cast
import django
from django.core.management.base import BaseCommand
from apps.word.models import Synonym, Translation, Word
from django.db.models import QuerySet

django.setup()


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        full_short_part_of_speech_name = {
            "существительное": "сущ",
            "прилагательное": "прил",
            "числительное": "числ",
            "местоимение": "мест",
            "глагол": "гл",
            "наречие": "нареч",
            "предикатив": "предик",
            "причастие": "прич",
            "деепричастие": "дееприч",
            "вводное слово": "вводн",
            "частица": "част",
            "междометие": "межд",
            "предлог": "предл",
            "неизменяемое": "неизм",
            "союз": "союз",  
            "иностранное слово": "иностр"
        }
        

        for full, short in full_short_part_of_speech_name.items():

            words_to_update = Translation.objects.filter(part_of_speech=full)
            print(words_to_update)

            for word in words_to_update:
                # word.part_of_speech = 1
                word.save()
