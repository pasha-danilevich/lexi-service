from django.conf import settings
import os
import json
from random import randint, choice


def get_time_on_lvl(user, current_lvl: int) -> int:
    second_in_day = 86400
    levels = user.settings['levels']

    day_in_lvl = levels[current_lvl-1]
    time = second_in_day * day_in_lvl
    return time


def is_last_level(user, current_lvl: int):
    levels = user.settings['levels']
    count_lvl = len(levels)

    if count_lvl == current_lvl:
        return True

    return False


def is_first_level(current_lvl: int):
    if current_lvl == 1:
        return True
    return False


class StaticFileContextManager:
    def __init__(self, filename, mode='r'):
        self.file_path = os.path.join(settings.STATIC_ROOT, filename)
        self.mode = mode

    def __enter__(self):
        self.file = open(self.file_path, self.mode, encoding='utf-8')
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()


def convert_part_of_speech(part_of_speech: str):
    part_set = {
        'verb': 'vb',
        'noun phrase': 'np',
        'noun': 'nn',
        'adverb': 'adv',
        'adjective': 'adj',
        'mix': 'mix'
    }
    part_of_speech = part_set.get(part_of_speech)

    if not part_of_speech:
        part_of_speech = part_set.get('mix')

    return part_of_speech


def get_false_set(instance, part_of_speech: str, number_of_false_set: int):

    file_names = ['FalseSet.json', 'FalseSet_2.json']
    file_name = file_names[randint(0, 1)]

    with StaticFileContextManager(file_name) as file:
        data_dict = json.loads(file.read())
        part_of_speech = convert_part_of_speech(part_of_speech)

        target_words_on_part = data_dict.get(part_of_speech)
        
        return generate_false_set(instance, target_words_on_part, number_of_false_set)


def generate_false_set(instance, word_list, number_of_false_set=4):
    false_set = []
    for _ in range(number_of_false_set):
        
        word = choice(word_list)
        text = word['val']
        
        if text == instance:
            continue
        
        word = {
            "text": text,
            "translation": choice(word['tr'])
        }
        false_set.append(word)

    return false_set
