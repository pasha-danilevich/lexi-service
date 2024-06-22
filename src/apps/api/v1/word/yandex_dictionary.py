import requests
from rest_framework.response import Response
from rest_framework import status


def fetch_word_data(text):
    url = "https://dictionary.yandex.net/api/v1/dicservice.json/lookup"
    params = {
        'key': 'dict.1.1.20240401T142057Z.dca24aa264de304c.6a1ba247e07408be736f729f72b1fe4d3d7e51cc',
        'lang': 'en-ru',
        'text': text,
        'ui': 'ru',
        # 'flag': 2
    }

    response = requests.get(url, params=params)
    if not response.status_code == 200:
        return None

    json_data = response.json()

    if not json_data['def']:
        return None

    word_set = {
        "word": extract_word(json_data),
        "translation": extract_translation(json_data),
        "synonym": extract_synonym(json_data),
        "meaning": extract_meaning(json_data)
    }

    return word_set


def extract_word(json: dict) -> dict:
    """
    Извлекает данные о слове из JSON-ответа.

    Args:
        json_data (dict): JSON-данные, содержащие информацию о слове.

    Returns:
        dict: Словарь с данными о слове.
    """

    word = json['def'][0]

    obj = {
        "text": word.get('text'),
        "part_of_speech": word.get('pos'),
        "transcription": word.get('ts'),
    }
    return convert_dict_value_to_lowercase(obj)


def extract_translation(json: dict) -> dict:
    words = json['def']
    # тут может быть множество переводов
    translations_list = []

    for word in words:
        translations = word.get('tr')
        if not translations:
            return None

        for translation in translations:

            obj = {
                "text": translation.get('text'),
                "part_of_speech": translation.get('pos'),
                "gender": translation.get('gen'),
                "frequency": translation.get('fr')
            }

            translations_list.append(convert_dict_value_to_lowercase(obj))

    return translations_list


def extract_synonym(json: dict) -> dict:
    words = json['def']
    # тут может быть множество переводов
    synonyms_list = []

    for word in words:
        translations = word.get('tr')
        if not translations:
            return None

        for translation in translations:
            synonyms = translation.get('syn')
            if not synonyms:
                continue

            for synonym in synonyms:

                obj = {
                    "text": synonym.get('text'),
                    "part_of_speech": synonym.get('pos'),
                    "gender": synonym.get('gen'),
                    "frequency": synonym.get('fr')
                }

                synonyms_list.append(convert_dict_value_to_lowercase(obj))
    if not synonyms_list:
        return None

    return synonyms_list


def extract_meaning(json: dict) -> dict:
    words = json['def']
    # тут может быть множество переводов
    meaning_list = []

    for word in words:
        translations = word.get('tr')
        if not translations:
            return None

        for translation in translations:
            meanings = translation.get('mean')
            if not meanings:
                continue

            for meaning in meanings:

                obj = {
                    "text": meaning.get('text')
                }

                meaning_list.append(convert_dict_value_to_lowercase(obj))
    if not meaning_list:
        return None

    return meaning_list


def convert_dict_value_to_lowercase(input_dict):
    """
    Преобразует все значения словаря к нижнему регистру.

    Args:
        input_dict (dict): Входной словарь.

    Returns:
        dict: Словарь с значениями в нижнем регистре.
    """
    result = {}
    for key, value in input_dict.items():
        try:
            result.update({key: value.lower()})
        except:
            result.update({key: value})

    return result


# print(fetch_word_data('get'))