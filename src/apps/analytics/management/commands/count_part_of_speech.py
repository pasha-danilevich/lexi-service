import django
from django.core.management.base import BaseCommand
from apps.word.models import PartOfSpeech, Translation
from apps.analytics.models import CountPartOfSpeech 

django.setup()

class Command(BaseCommand):
    """
    Команда для подсчета слов в таблице Translation по каждой части речи
    и обновления или создания записей в таблице CountPartOfSpeech.

    Команда выполняет следующие действия:
    1. Получает все записи из таблицы PartOfSpeech.
    2. Для каждой части речи:
        - Считает количество связанных записей в таблице Translation.
        - Пытается обновить существующую запись в таблице CountPartOfSpeech
          с новым значением count. Если записи нет, создает новую.
    3. Выводит сообщение об успешном создании или обновлении записи в CountPartOfSpeech.

    Пример использования:
        python manage.py count_part_of_speech
    """
    help = 'Count words in Translation by PartOfSpeech and update CountPartOfSpeech'


    def handle(self, *args, **options):
        # Получаем все части речи
        parts_of_speech = PartOfSpeech.objects.all()

        for part in parts_of_speech:
            # Считаем количество переводов для текущей части речи
            count = Translation.objects.filter(part_of_speech=part).count()

            # Пытаемся обновить или создать запись в CountPartOfSpeech
            count_part_of_speech, created = CountPartOfSpeech.objects.update_or_create(
                part_of_speech=part,
                defaults={'count': count}
            )

            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'Created CountPartOfSpeech for {part.text} with count {count}'
                ))
            else:
                self.stdout.write(self.style.SUCCESS(
                    f'Updated CountPartOfSpeech for {part.text} with count {count}'
                ))
        