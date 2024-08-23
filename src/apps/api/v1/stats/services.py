from django.db.models import Q
from datetime import datetime, timedelta

    
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

def _count_occurrences(arr, n):
    result = [0] * n
    for num in arr:
        if num <= n:
            result[num - 1] += 1
    return result


def get_words_count_on_levels(levels_length: int, training_list) -> list:
    lvl_list = []
    for training in training_list:
        lvl_list.append(training.lvl)
    result = _count_occurrences(lvl_list, levels_length)
    return result