import requests
from rest_framework.response import Response
from rest_framework import status
from config.local_settings import Y_KEY


from datetime import datetime

def record_execution_time(func):
    def wrapper(*args, **kwargs):
        time_start = datetime.now()
        result = func(*args, **kwargs)
        time_end = datetime.now()
        execution_time = time_end - time_start
        sec_milisec_execution_time = str(execution_time).split(':')[-1]
        return result, sec_milisec_execution_time
    return wrapper

@record_execution_time        
def get_response(url, params):
    return requests.get(url, params=params)

def fetch_word_data(word: str):
    url = "https://dictionary.yandex.net/api/v1/dicservice.json/lookup"
    
    if not word:
        return None
    
    params = {
        'key': Y_KEY,
        'lang': 'en-ru',
        'text': word,
        'ui': 'ru',
        'flags': 2
    }

    response, execution_time = get_response(url, params=params)
    
    
    
    if not response.status_code == 200: # type: ignore
        return None

    json_data = response.json() # type: ignore
    is_empty_response = False if json_data['def'] else True
    
    
    
    # Логирование
    time = datetime.now().strftime('%m-%d-%H-%M-%S')
    status_code = '404' if is_empty_response else '200'
    
    log_data = f"{time} {status_code} {execution_time} {word.lower()}"
    with open("yandex_dictionary_log.txt", "a") as log_file:
        log_file.write(log_data + "\n")
        
    if is_empty_response:
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


def extract_translation(json: dict) -> list | None:
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


def extract_synonym(json: dict) -> list | None:
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


def extract_meaning(json: dict) -> list | None:
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

