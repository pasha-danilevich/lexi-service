from typing import Any

from datetime import datetime

def _is_valid_date(date_string: str) -> bool:
    """
    Проверяет, соответствует ли строка формату даты ГГГГ-ММ-ДД.

    Args:
        date_string (str): Строка, представляющая дату.

    Returns:
        bool: True, если строка соответствует формату даты, иначе False.
    """
    try:
        # Пытаемся преобразовать строку в объект datetime
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        # Если возникает ошибка, значит формат неверный
        return False


def _check_allowed(order: str, direction: str):
    ALLOWED_ORDER_FIELDS = ['lvl_sum', 'date_added', 'word_text']
    ALLOWED_DIRECTION = ['DESC', 'ASC']
    
    if order not in ALLOWED_ORDER_FIELDS:
        raise ValueError(f"Invalid order field: {order}")
    if direction not in ALLOWED_DIRECTION:
        raise ValueError(f"Invalid order direction: {direction}")

def _create_filters_list(filters: list[str], values: list[str | int]) -> list[str]:
    """
    Создает список фильтров на основе переданных списков фильтров и значений.

    Args:
        filters (list[str]): Список фильтров.
        values (list[str | int]): Список значений.

    Returns:
        list[str]: Список строк фильтров.

    Raises:
        ValueError: Если формат даты неверный.
    """
    filters_list = []

    for i in range(len(filters)):
        filter_item = filters[i]
        value_item = values[i]

        if filter_item in ['lvl_sum', 'part_of_speech']:
            filters_list.append(f" {filter_item} = '{value_item}' ")
        elif filter_item == 'form':
            filters_list.append(f' {filter_item} IS NOT NULL ')
        elif filter_item == 'date_added':
            value_item = str(value_item)
            if _is_valid_date(value_item):
                filters_list.append(
                    f" {filter_item} >= '{value_item} 00:00:00' AND {filter_item} <= '{value_item} 23:59:59' "
                )
            else:
                raise ValueError("Неправильный формат даты. Нужен ГГГГ-ММ-ДД")
    
    return filters_list

def get_query(
    filter: list = [], 
    value: list = [],
    order: str = 'date_added', 
    direction: str = 'DESC' 
    ):
    _check_allowed(order=order, direction=direction)
    
    WHERE = ''
    filters = ''
    
    filters_list = _create_filters_list(filter, value)
        
    if filters_list:
        WHERE = 'WHERE' 
        if len(filters_list) > 1:
            filters = " AND ".join(filters_list)
        else:
            filters = filters_list[0]
    
    query = f"""
SELECT *
FROM (
    SELECT DISTINCT ON (w.id)
        wd.id, 
        wd.date_added AS date_added,
        w.id AS word_id,
        w.form AS form,
        w.transcription,
        w.text AS word_text,
        wp.text AS part_of_speech,
        COALESCE(SUM(wt.lvl), 0) / %s AS lvl_sum,
        CASE 
            WHEN word_counts.word_count > 1 THEN TRUE
            ELSE FALSE
        END AS is_many
    FROM 
        public.word_dictionary wd
    JOIN 
        word_word w ON wd.word_id = w.id
    JOIN 
        word_partofspeech wp ON w.part_of_speech_id = wp.id
    LEFT JOIN 
        word_training wt ON wd.id = wt.dictionary_id
    LEFT JOIN (
        SELECT 
            word_id, 
            COUNT(*) AS word_count
        FROM 
            public.word_dictionary
        GROUP BY 
            word_id
    ) AS word_counts ON w.id = word_counts.word_id
    WHERE 
        wd.user_id = %s
    GROUP BY 
        wd.id, wd.date_added, w.id, wp.text, w.form, w.transcription, word_counts.word_count
) AS subquery
{WHERE}
{filters}
ORDER BY 
    {order} {direction};  -- Динамическое поле сортировки
"""
    return query