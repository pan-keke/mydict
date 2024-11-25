from django.shortcuts import render, redirect
import csv
import re
from pathlib import Path


# Домашняя страница
def home(request):
    return render(request, 'home.html')


# Страница для списка слов
def words_list(request):
    words = []
    csv_path = Path('words.csv')

    # Если файл не существует, создаём его
    if not csv_path.exists():
        with open('words.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['слово', 'перевод'])  # Заголовки файла

    # Чтение данных из файла
    with open('words.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # Пропускаем заголовки
        for row in reader:
            words.append({'word': row[0], 'translation': row[1]})

    return render(request, 'words_list.html', {'words': words})


def is_valid_word(word):
    return re.match(r"^[^\d]+$", word) is not None


# Страница для добавления слов
def add_word(request):
    if request.method == 'POST':
        word = request.POST['word1'].strip().lower()  # Приводим к единому формату (строчные буквы)
        translation = request.POST['word2'].strip().lower()

        # Проверка на валидность слова
        if not is_valid_word(word) or not is_valid_word(translation):
            return render(request, 'add_word.html', {
                'error': 'Слово и перевод не должны содержать цифры и символы!'
            })

        # Проверка на дубликаты
        with open('words.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if word == row[0] and translation == row[1]:
                    return render(request, 'add_word.html', {
                        'error': 'Это слово уже есть в словаре!'
                    })

        # Если всё корректно, добавляем в файл
        with open('words.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([word, translation])

        return redirect('home')

    return render(request, 'add_word.html')
