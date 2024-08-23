from apps.word.models import Training
from apps.word.utils import get_current_unix_time
from config.settings import TRAINING_TYPES


def create_traning_for_word(word):

    time = get_current_unix_time()
    count_training_type = len(TRAINING_TYPES)

    data = [{'dictionary': word, 'type_id': type_id, 'time': time}
            for type_id in range(1, count_training_type + 1)]

    Training.objects.bulk_create([Training(**item) for item in data])
