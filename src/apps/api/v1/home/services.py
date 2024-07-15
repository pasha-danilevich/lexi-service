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