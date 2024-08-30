from random import randint, choice

from apps.word.utils import get_current_unix_time


def _get_time_on_lvl(levels, current_lvl: int) -> int:
    second_in_day = 86400
    try:
        day_in_lvl = levels[current_lvl-1]
    except IndexError:  # если индекс больше или меньше существуещего, то ставим последнюю дату
        day_in_lvl = levels[-1]

    time = second_in_day * day_in_lvl
    return time


def _is_last_level(levels, current_lvl: int):
    count_lvl = len(levels)

    if count_lvl <= current_lvl:
        return True

    return False


def _is_first_level(current_lvl: int):
    if current_lvl == 1:
        return True
    return False

def get_new_lvl(is_correct, levels, current_lvl) -> int:
    if is_correct:
        if not _is_last_level(levels, current_lvl):
            new_lvl = current_lvl + 1
        else:
            # остается на прежднем уровне (1й или последний)
            new_lvl = current_lvl
            
    else:
        if not _is_first_level(current_lvl):
            new_lvl = current_lvl - 1
        else:
            # остается на прежднем уровне (1й или последний)
            new_lvl = current_lvl

    return new_lvl

def get_new_time(levels, new_lvl):
    return get_current_unix_time() + _get_time_on_lvl(levels, new_lvl)
