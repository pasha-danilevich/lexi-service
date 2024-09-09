from typing import Any
from apps.word.models import Training
from apps.word.utils import get_current_unix_time
from config.settings import TRAINING_TYPES


def create_traning_for_word(word):

    time = get_current_unix_time()
    count_training_type = len(TRAINING_TYPES)

    data = [{'dictionary': word, 'type_id': type_id, 'time': time}
            for type_id in range(1, count_training_type + 1)]

    Training.objects.bulk_create([Training(**item) for item in data])


def make_dict(tulple_list: list[tuple[Any, ...]]) -> list[dict[str, Any]]:
    
    dict_result = [
        {
        'id': item[0],
        'date_added': item[1],
        'word_id': item[2],
        'word_form': item[3],
        'word_transcription': item[4],
        'word_text': item[5],
        'part_of_speech': item[6],
        'lvl_sum': item[7],
        'is_many': item[8]
        }
        for item in tulple_list
    ]  
    return dict_result


def get_params_dict(params) -> dict[str, Any]:
    result = {}
    
    order = params.get('order', None) 
    if order:
        result.update({'order': order})
    
    direction = params.get('direction', None) 
    if direction:
        result.update({'direction': direction})

    filter: list = params.getlist('filter')
    value: list = params.getlist('value') 
    
    # Проверяем, что длины массивов совпадают и они не пустые
    if len(filter) != len(value):
        raise ValueError("Кол-во параметров filter и value не совпадают. Параметры filter и value надо передавать вместе")
        
    
    if filter and value:
        result.update({'filter': filter})
        result.update({'value': value})
     
    return result
    