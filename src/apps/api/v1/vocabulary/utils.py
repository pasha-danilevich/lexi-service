def _count_occurrences(arr, n):
    result = [0] * n
    for num in arr:
        if num <= n:
            result[num - 1] += 1
    return result

def get_words_count_on_levels(type: str, levels_length: int, queryset) -> list:
    lvl_list = list(queryset.values_list(type, flat=True))

    result = _count_occurrences(lvl_list, levels_length)
    return result

# def get_words_count_on_levels(type: str, levels_length: int, queryset) -> list:
#     lvl_list = []
#     for lvl in range(1, levels_length + 1):
#         words_count = queryset.filter(**{type: lvl}).count()
#         lvl_list.append(words_count)
#     return lvl_list