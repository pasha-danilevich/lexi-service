file_path: str = r"C:\Users\Pavel\Desktop\Code\DRF\read-recall\src\yandex_dictionary_log.txt"
# Чтение исходного файла
with open(file_path, "r") as source_file:
    lines = source_file.readlines()

# Фильтрация строк с кодом состояния 404
filtered_lines = [line for line in lines if "404" in line]

# Извлечение слов из каждой строки
words = []
for line in filtered_lines:
    parts = line.split()
    if len(parts) >= 3:
        word = parts[3]
        words.append(word)

# Запись слов в новый файл
with open("404_words.txt", "w") as target_file:
    target_file.write(" ".join(words))

print(f"Слова успешно записаны в файл '404_words.txt'!")

