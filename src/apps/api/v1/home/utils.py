from datetime import datetime
from django.db.models import Q


def get_beginning_day():
    date = datetime.now()
    beginning_day = date.replace(second=0, microsecond=0, minute=0, hour=0)
    
    return int(beginning_day.timestamp())

def get_ending_day():
    unix_day = 86400
    beginning_day = get_beginning_day()
    
    return beginning_day + unix_day



def get_new_words_today(user_words, beginning_day, ending_day):
    """
    Получает новые слова, добавленные сегодня для данного пользователя.
    
    Аргументы:
        dictionary (QuerySet): Queryset объектов Dictionary для данного пользователя.
        beginning_day (datetime): Начало текущего дня.
        ending_day (datetime): Конец текущего дня.
        
    Возвращает:
        QuerySet: Queryset новых слов, добавленных сегодня для данного пользователя.
    """
    return user_words.filter(
        Q(recognize_time__gte=beginning_day) & Q(recognize_time__lte=ending_day)
    )


def get_list_words(queryset):
    word_list = []
    for user_word_relationship in queryset:
        user_word = user_word_relationship.word
        obj = {
            'text': user_word.text,
            'date_added': user_word_relationship.date_added
        }
        
        word_list.append(obj)
    return word_list