from django.db.models import Q
from datetime import datetime, timedelta

def get_new_words_today(dictionary):
    """
    Получает новые слова, добавленные сегодня для данного пользователя.
    
    Аргументы:
        dictionary (QuerySet): Queryset объектов Dictionary для данного пользователя.

    Возвращает:
        QuerySet: Queryset новых слов, добавленных сегодня для данного пользователя.
    """
    today = datetime.now().date()
    beginning_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = beginning_of_day + timedelta(days=1)
    
    return dictionary.filter(
        **{'date_added__gte': beginning_of_day, 'date_added__lt': end_of_day}
    )
    
def get_list_words(dictionary):
    word_list = []
    for word_obj in dictionary:
        word = word_obj.word
        translation = word_obj.translation
        obj = {
            'text': word.text,
            'translation': translation.text,
            'date_added': word_obj.date_added
        }
        
        word_list.append(obj)
    return word_list