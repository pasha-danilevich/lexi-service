from apps.word.models import Training, TrainingType
from apps.word.utils import get_current_unix_time


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

def create_traning_for_word(word):

    time = get_current_unix_time()
    type_queryset = TrainingType.objects.all()
    
    data = [{'dictionary': word, 'type': type, 'time': time} for type in type_queryset]
    Training.objects.bulk_create([Training(**item) for item in data])    
