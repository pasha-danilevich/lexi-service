import requests
from rest_framework.response import Response
from rest_framework import status  

def fetch_word_data(text):
    url = "https://dictionary.yandex.net/api/v1/dicservice.json/lookup"
    params = {
        'key': 'dict.1.1.20240401T142057Z.dca24aa264de304c.6a1ba247e07408be736f729f72b1fe4d3d7e51cc',
        'lang': 'en-ru',
        'text': text,
        'ui': 'en',
        # 'flag': 2
    }
    
    response = requests.get(url, params=params)
    
    if not response.status_code == 200:
        return None
    
    json_data = response.json() 
    
    if not json_data['def']:
        return None, None
     
    word = extract_word_data(json_data)

    return word, json_data
    
        
def extract_word_data(json_data: dict) -> dict:
    """
    Извлекает данные о слове из JSON-ответа.
    
    Args:
        json_data (dict): JSON-данные, содержащие информацию о слове.
        
    Returns:
        dict: Словарь с данными о слове.
    """
    
    word = json_data['def'][0]
    translation = word['tr'][0]
    synonyms_list = make_synonyms_list(translation.get('syn', None))
    
    data = {
        "text": word.get('text'),
        "part": word.get('pos'),
        "transcription": word.get('ts'),
        "translation": translation.get('text'),
        "synonym": synonyms_list
    }
    return convert_dict_value_to_lowercase(data) 


def make_synonyms_list(synonyms: dict) -> list:
    if not synonyms:
        return None
    synonyms_list = [word['text'].lower() for word in synonyms]
    return synonyms_list

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
