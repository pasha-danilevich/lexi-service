def transliterate(text:str) -> str:
    """
    Функция транслитерирует строку из кириллицы в латиницу без использования сторонних библиотек.

    :param text: строка на кириллице
    :return: транслитерированная строка на латинице
    """
    transliteration = {
        'а': 'a',
        'б': 'b',
        'в': 'v',
        'г': 'g',
        'д': 'd',
        'е': 'e',
        'ё': 'yo',
        'ж': 'zh',
        'з': 'z',
        'и': 'i',
        'й': 'j',
        'к': 'k',
        'л': 'l',
        'м': 'm',
        'н': 'n',
        'о': 'o',
        'п': 'p',
        'р': 'r',
        'с': 's',
        'т': 't',
        'у': 'u',
        'ф': 'f',
        'х': 'h',
        'ц': 'c',
        'ч': 'ch',
        'ш': 'sh',
        'щ': 'sch',
        'ы': 'y',
        'э': 'e',
        'ю': 'yu',
        'я': 'ya',
    }

    result = ''
    text = text.lower()
    for symbol in text:
        if symbol in transliteration:
            result += transliteration[symbol]
        else:
            result += symbol

    return result
