import re

def clean_string(text):
    """
    Очищает строку, оставляя только буквы.
    
    Args:
        text (str): Входная строка.
        
    Returns:
        str: Очищенная строка, содержащая только буквы.
    """
    return re.sub(r'[^a-zA-Zа-яА-Я]', '', text)
