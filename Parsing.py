import re
from collections import Counter


def remove_html_tags(text):
    # Удаление всех HTML тегов из текста
    return re.sub(r'<[^>]+>', '', text)


def extract_words(text):
    # Сортировка слов по длине
    words = re.findall(r'\b[a-zA-Zа-яА-Я]{3,}\b', text)
    return words


def main():
    # Запрос пути к HTML файлу
    file_path = input("Введите путь к HTML файлу: ")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        clean_text = remove_html_tags(html_content)
        words = extract_words(clean_text.lower())
        word_counts = Counter(words)

        print("Топ 10 наиболее часто встречающихся слов:")
        for word, count in word_counts.most_common(10):
            print(f"{word}: {count}")

    except FileNotFoundError:
        print(f"Файл по пути {file_path} не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
