def get_page_from_context(context: dict[any, any]) -> int:
    """
    Извлекает номер страницы из контекста запроса.
    
    Функция предполагает, что номер страницы передается в URL-адресе
    в качестве последнего элемента пути. Например:
    
    /some/path/2
    
    Где 2 - номер страницы.
    
    Args:
        context (dict[any, any]): Словарь контекста запроса.
        
    Returns:
        int: Номер страницы, извлеченный из контекста. Нумерация начинается с 0.
    """
    full_path = context['request'].get_full_path()
    page = int(full_path.split('/')[-1]) - 1
    return page

