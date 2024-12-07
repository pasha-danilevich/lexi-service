from typing import Any
from django.db import IntegrityError, transaction
import re

from googletrans import Translator

from apps.api.v1.word.yandex_dictionary import fetch_word_data
from apps.user.models import User
from apps.word.models import Meaning, Synonym, Translation, Word


def clean_string(text) -> str:
    """
    Очищает строку, оставляя только буквы.

    Args:
        text (str): Входная строка.

    Returns:
        str: Очищенная строка, содержащая только буквы.
    """
    return re.sub(r'[^a-zA-Zа-яА-Я]', '', text)


def word_bulk_create(cls, word_set: dict, word: Word):
    if not word_set:
        return None

    for obj in word_set:
        obj.update({"word": word})
        obj = cls.objects.create(**obj)


def get_or_create_word(request_word: str) -> tuple[Word | None, bool]:
    """
    Получает или создает слово в базе данных.

    Аргументы:
    request_word (str): Строка, представляющая слово для поиска или создания.

    Возвращает:
    tuple[Word | None, bool]: Кортеж, содержащий объект модели Word, если слово найдено или создано, и булевое значение, указывающее, было ли слово создано (True) или найдено (False). Если слово не найдено и не может быть создано, возвращается (None, False).

    Исключения:
    - Word.DoesNotExist: Если слово не найдено в базе данных и не может быть создано.
    - Другие исключения, связанные с базой данных или внешними API.

    Примечания:
    - Если request_word равен None или пустой строке, функция возвращает (None, False).
    - Функция использует методы get() и create() модели Word для поиска и создания слов.
    - Если слово создается, связанные данные (перевод, синоним, значение) также создаются с помощью вспомогательных функций word_bulk_create().
    """
    created = True
    if not request_word:
        return None, False
    try:
        word = Word.objects.get(text=request_word)
        created = False
        return word, created

    except Word.DoesNotExist:

        word_set = fetch_word_data(request_word)

        if not word_set:
            word_set = make_word_set_on_google_translater(text=request_word)

        print(word_set)
        try:
            with transaction.atomic():
                word = Word.objects.create(**word_set['word'])

                word_bulk_create(Translation, word_set['translation'], word)
                word_bulk_create(Synonym, word_set['synonym'], word)
                word_bulk_create(Meaning, word_set['meaning'], word)

        except IntegrityError:  # Если возникла ошибка уникальности, пытаемся получить существующее слово

            existing_word = Word.objects.get(text=word_set['word']['text'])
            created = False

            return existing_word, created

        except Exception as e:
            raise e

        return word, created


def get_related_pk(word: Word, user: User) -> list[int]:

    # Получаем все слова из словаря пользователя
    user_dictionary_words = word.dictionary.all(user_id=user.pk)

    if user_dictionary_words:
        # Возвращаем список первичных ключей переводов, которые добавлял пользователь
        return [
            dictionary_word.translation.pk
            for dictionary_word in user_dictionary_words
        ]
    else:
        return []


def google_translater(text: str) -> str:
    dest_language = 'ru'

    translator = Translator()

    translation = translator.translate(text, dest=dest_language)
    translated_text = translation.text  # type: ignore
    return translated_text



def make_word_set_on_google_translater(text: str) -> dict[str, Any]:
    translate = google_translater(text=text)
    word_set = {
        'word': {
            'text': text,
            'part_of_speech': None,
            'transcription': None,
            'form': None
        },
        'translation': [
            {'text': translate,
             'part_of_speech': None,
             'gender': None,
             'frequency': None}
        ],
        'synonym': None,
        'meaning': None
    }
    return word_set
