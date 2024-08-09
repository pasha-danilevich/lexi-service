import time

def get_current_unix_time() -> int:
    """
    Возвращает текущее время в формате Unix timestamp.
    
    Returns:
        int: Текущее время в секундах с 1 января 1970 года.
    """
    return round(time.time())
    
def get_key_by_value(training_types, value_to_find):
    for key, value in training_types.items():
        if value == value_to_find:
            return key
    return None