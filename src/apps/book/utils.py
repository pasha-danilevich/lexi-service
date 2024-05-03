from config.settings import PAGE_SIZE, PENALTY_SIZE

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



def _get_line_length(line: str, page_size: int, penalty: int) -> int:
    """
    Рассчитывает длину строки на странице, учитывая штраф за короткие строки.

    Аргументы:
        line (str): Строка, для которой рассчитывается длина.
        page_size (int): Текущий размер страницы.
        penalty (int): Штраф за короткую строку.

    Возвращает:
        int: Обновленный размер страницы.
    """
    # penalty for a short line
    if len(line) < 25:
        page_size += penalty 
    else:
        page_size += len(line)
    return page_size

   

def _get_page(file):
    """
    Читает страницу из файла, учитывая размер страницы и штраф за перенос строк.

    Args:
        file: Открытый файл для чтения.

    Returns:
        tuple: Кортеж, содержащий страницу и флаг, указывающий, является ли страница последней в файле.
    """
    page_size = 0 
    page = []
    while page_size < PAGE_SIZE:
        line = file.readline()
        
        if not line:
            return (page, True)
        
        if line == '\n':
            continue
        
        if line[-1] == '\n':
            line = line[:-1]
        
        page_size = _get_line_length(line, page_size, PENALTY_SIZE)

        page.append(line)
        
    else:  
        return (page, False)


def txt_to_book(path):
    """
    Преобразует текстовый файл в список страниц.

    Args:
        path (str): Путь к текстовому файлу.

    Returns:
        list: Список страниц, представляющих книгу.
    """
    book = []  
    
    with open(path, 'r') as file:
        while True:
            page, is_end = _get_page(file)
            book.append(page)
            if is_end:
                break
    return book




def _make_lines(text: str):      
    """
    Принимает текст и разбивает его на строки по символу новой строки.
    
    Args:
        text (str): Входной текст для разбиения на строки.
    
    Yields:
        str: Каждая строка текста из входного текста.
    """
    lines = text.split('\n')
    for line in lines:
        if line:
            yield line


def _make_page(lines_generator):
    """
    Генерирует страницы из строк, учитывая размер страницы и штраф за перенос строк.
    
    Args:
        lines_generator: Генератор строк.
    
    Yields:
        list: Список строк, представляющих страницу.
    """
    page_size = 0 
    page = []
    for line in lines_generator:
        if page_size < PAGE_SIZE: 
            page_size = _get_line_length(line, page_size, PENALTY_SIZE)
            page.append(line)
        else:
            yield page
            page_size = 0 
            page = []
    else:
        yield page
            

def json_to_book(text: str):
    """
    Преобразует JSON с книгой в список страниц.
    
    Args:
        text (str): json srtingify текст книги.
    
    Returns:
        list: Список страниц, представляющих книгу.
    """
    book = []
    lines_generator = _make_lines(text)
    pages_generator = _make_page(lines_generator)
    for page in pages_generator:
        book.append(page)
    else:
        return book