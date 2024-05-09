import requests

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
    
    if response.status_code == 200:
        json_data = response.json()
    else:
        None
        
    word = extract_word_data(json_data)
    return word

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
    
    data = {
        "text": word['text'],
        "part": word['pos'],
        "transcription": word['ts'],
        "translation": translation['text']
    }
    
    return data
