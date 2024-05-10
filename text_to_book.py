

PAGE_SIZE = 2000
PENALTY_SIZE = 100

path = 'C:\\Users\\Pavel\\Desktop\\book.txt'
json = {
    'title': 'Mr. Hicks 2', 
    'author': 'Alexie Aaron', 
    'page_count': 89, 
    'book': '' 
    }


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





def make_lines(text: str):      
    lines = text.split('\n')
    for line in lines:
        if line:
            yield line


def make_page(lines_generator):
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
            

 

def json_to_book(json: dict):
    book = []
    lines_generator = make_lines(json['book'])
    pages_generator = make_page(lines_generator)
    for page in pages_generator:
        book.append(page)
    else:
        return book

    