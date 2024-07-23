from io import TextIOWrapper
import random
import time
import django
from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import reverse
import requests
import signal

from apps.api.v1.word.services import clean_string
from apps.word.models import Word

django.setup()

class Command(BaseCommand):
    help = 'Парсинг слов в бд'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.duration = 10
        self.limit = 5000
        self.file_path = None
        self.count_fetch = 0
        self.interrupted = False
        self.count_word = 0

    def add_arguments(self, parser):
        parser.add_argument('--file_path', type=str)

    def handle(self, *args, **options):
        signal.signal(signal.SIGINT, self.interrupt_handler)

        self.file_path = options.get('file_path')

        if not self.file_path:
            self.stdout.write(self.style.ERROR(f'Нужен путь к файлу. --file_path'))

        word_create_url = settings.SITE_URL + reverse('word-create')

        with open(self.file_path, 'r') as file:
            while True:
                if self.interrupted:
                    break
                line = file.readline()
                if not line:
                    break
                words = line.strip().split()
                for word in words:
                    self.count_word += 1
                    
                    if self.count_fetch >= self.limit:
                        break
                    
                    if self.interrupted:
                        break
                    
                    word = clean_string(word).lower()
                    
                    if self.is_word_exists(word):
                        self.stdout.write(self.style.HTTP_INFO(f'"{word}" уже было создано'))
                        continue
                    
                    self.create_word(word, word_create_url)
                
        self.clear_passed_words(self.count_word)
        self.stdout.write(self.style.SUCCESS(f'"{self.count_fetch}" запросов в Y-DICT'))
        self.stdout.write(self.style.SUCCESS(f'"{self.count_word}" слов пройдено'))
        
        
    def interrupt_handler(self, signal, frame):
        self.interrupted = True
        self.stdout.write(self.style.WARNING(f'Программа прервана пользователем'))

    def is_word_exists(self, word: str) -> bool:
        try:
            Word.objects.get(text=word)
            return True
        except Word.DoesNotExist:
            return False

    def create_word(self, word: str, word_create_url: str):
        data = {"word": word}
        time.sleep(self.duration)
        response = requests.post(word_create_url, data=data)
        self.print_response(response, word)
        self.count_fetch += 1

    def print_response(self, response, word):
        if response.status_code == 201:
            self.stdout.write(self.style.SUCCESS(f'"{word}" успешно создано'))
        elif response.status_code == 404:
            self.stdout.write(self.style.HTTP_NOT_FOUND(f'"{word}" не найдено'))
        elif response.status_code == 500:
            self.stdout.write(self.style.ERROR(f'Ошибка 500 при создании слова "{word}"'))
            
    def clear_passed_words(self, count_word: int):
        # Открываем файл для чтения
        with open(self.file_path, 'r') as file:
            # Читаем все строки из файла
            lines = file.readlines()
        
        # Находим индекс строки, содержащей count_word-ое слово
        word_count = 0
        for i, line in enumerate(lines):
            words = line.strip().split()
            word_count += len(words)
            if word_count >= count_word:
                start_index = i
                break
        else:
            # Если count_word больше общего количества слов в файле, ничего не делаем
            return
        
        # Записываем в файл строки, начиная с найденной строки
        with open(self.file_path, 'w') as file:
            file.writelines(lines[start_index:])
            
