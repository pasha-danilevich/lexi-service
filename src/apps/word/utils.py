import time

def get_current_unix_time() -> int:
    """
    Возвращает текущее время в формате Unix timestamp.
    
    Returns:
        int: Текущее время в секундах с 1 января 1970 года.
    """
    return round(time.time())
    
