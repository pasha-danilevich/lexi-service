from typing import cast

from config.settings import TRAINING_TYPES_ID



def create_lvl_list(counted_word, initial_list, type_id: int, number_iteration):
    for i, entry in enumerate(counted_word):
        if entry['type_id'] == type_id:
            initial_list[i] = entry['word_count'] 
            number_iteration[0] += 1  # Изменяем значение в списке
        else:
            break  
    return initial_list  
