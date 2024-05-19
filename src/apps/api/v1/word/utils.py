import re

from apps.api.v1.word.yandex_dictionary import fetch_word_data
from apps.word.models import Meaning, Synonym, Translation, Word


def clean_string(text):
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



def get_or_create_word(request_word):
    try:
        word = Word.objects.get(text=request_word)
        return word
    except Word.DoesNotExist:
        word_set = fetch_word_data(request_word)

        if not word_set:
            return None

        word = Word.objects.create(**word_set['word'])

        word_bulk_create(Translation, word_set['translation'], word)
        word_bulk_create(Synonym, word_set['synonym'], word)
        word_bulk_create(Meaning, word_set['meaning'], word)

        return word


def check_related_user(word, user):

    if word.users.exists():

        user_related_word = user.words.all()

        if user_related_word.filter(word_id=word.id).exists():

            return True

    return False
