import json
from difflib import unified_diff

def compare_results(gemini_file, mistral_file):
    # Открываем файлы с явным указанием кодировки UTF-8
    with open(gemini_file, 'r', encoding='utf-8') as f1, open(mistral_file, 'r', encoding='utf-8') as f2:
        gemini_results = [json.loads(line) for line in f1 if line.strip()]
        mistral_results = [json.loads(line) for line in f2 if line.strip() and 'error' not in json.loads(line)]

    # Проверяем, что есть данные для сравнения
    if not gemini_results:
        print("Ошибка: файл Gemini пуст или содержит некорректные данные")
        return
    if not mistral_results:
        print("Ошибка: файл Mistral пуст или содержит только ошибки")
        return

    # Сравнение структуры
    print("Сравнение структуры JSON:")
    gemini_keys = set(gemini_results[0].keys())
    mistral_keys = set(mistral_results[0].keys())
    print(f"Gemini keys: {gemini_keys}")
    print(f"Mistral keys: {mistral_keys}")
    print(f"Разница: {gemini_keys - mistral_keys}")

    # Сравнение конкретных значений
    print("\nСравнение значений для ПЖВ1:")
    try:
        gemini_sample = next(item for item in gemini_results if item.get('name', '').startswith('ПЖВ1'))
        mistral_sample = next((item for item in mistral_results if item.get('name', '').startswith('ПЖВ1')), None)
        
        if mistral_sample:
            for key in gemini_sample:
                print(f"\nПоле: {key}")
                print(f"Gemini: {gemini_sample[key]}")
                print(f"Mistral: {mistral_sample.get(key, 'N/A')}")
        else:
            print("Mistral не смог обработать ПЖВ1")
    except StopIteration:
        print("Не найдено записи ПЖВ1 в файле Gemini")

    # Подсчет ошибок парсинга
    with open(mistral_file, 'r', encoding='utf-8') as f:
        errors = sum(1 for line in f if 'error' in json.loads(line))
    print(f"\nОшибок парсинга у Mistral: {errors}/{len(gemini_results)}")

# Запуск сравнения
compare_results(
    r'C:\Users\annoy\Downloads\Telegram Desktop\gribito_nadristito\gribito_nadristito\output.txt',
    r'C:\Users\annoy\Downloads\Telegram Desktop\gribito_nadristito\gribito_nadristito\mistral_output.txt'
)