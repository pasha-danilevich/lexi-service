VOCABULARY_QUERY = """
SELECT *
FROM (
    SELECT DISTINCT ON (w.id)  -- Уникальные записи по полю word_id
        wd.id, 
        wd.date_added,
        w.id AS word_id,
        w.form,
        w.transcription,
        w.text AS word_text,
        wp.text AS part_of_speech,
        COALESCE(SUM(wt.lvl), 0) / %s AS lvl_sum,  -- Делим сумму уровней на переданный параметр
        CASE 
            WHEN word_counts.word_count > 1 THEN TRUE  -- Если больше 1, то is_many = true
            ELSE FALSE
        END AS is_many
    FROM 
        public.word_dictionary wd
    JOIN 
        word_word w ON wd.word_id = w.id  -- JOIN на word_word
    JOIN 
        word_partofspeech wp ON w.part_of_speech_id = wp.id  -- JOIN на word_partof_speech
    LEFT JOIN 
        word_training wt ON wd.id = wt.dictionary_id  -- Используем LEFT JOIN, чтобы получить все записи из word_dictionary
    LEFT JOIN (
        SELECT 
            word_id, 
            COUNT(*) AS word_count
        FROM 
            public.word_dictionary
        GROUP BY 
            word_id
    ) AS word_counts ON w.id = word_counts.word_id  -- Подзапрос для подсчета количества слов
    WHERE 
        wd.user_id = %s
    GROUP BY 
        wd.id, wd.date_added, w.id, wp.text, w.form, w.transcription, word_counts.word_count
) AS subquery
ORDER BY 
    date_added DESC  -- Сортируем по date_added
"""