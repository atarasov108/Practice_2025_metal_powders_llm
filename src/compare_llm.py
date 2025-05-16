import json
from collections import defaultdict

def format_value(value, indent=0):
    """Форматирует значение для читаемого вывода"""
    if isinstance(value, dict):
        return "{\n" + "\n".join(f"{' '*(indent+4)}{k}: {format_value(v, indent+4)}" for k, v in value.items()) + f"\n{' '*indent}}}"
    elif isinstance(value, list):
        return "[\n" + "\n".join(f"{' '*(indent+4)}{format_value(item, indent+4)}" for item in value) + f"\n{' '*indent}]"
    else:
        return str(value)

def compare_lists(gemini_list, mistral_list, path):
    """Детально сравнивает два списка"""
    differences = []
    max_len = max(len(gemini_list), len(mistral_list))
    
    for i in range(max_len):
        item_path = f"{path}[{i}]"
        
        # Проверка наличия элемента в обоих списках
        if i >= len(gemini_list):
            differences.append(f"{item_path}: Отсутствует в Gemini (Mistral: {format_value(mistral_list[i])})")
            continue
        if i >= len(mistral_list):
            differences.append(f"{item_path}: Отсутствует в Mistral (Gemini: {format_value(gemini_list[i])})")
            continue
            
        # Полное сравнение элементов
        differences.extend(compare_structures(gemini_list[i], mistral_list[i], item_path))
    
    return differences

def compare_structures(gemini_val, mistral_val, path=""):
    """Рекурсивно сравнивает структуры и возвращает различия"""
    differences = []
    
    # Сравнение типов
    if type(gemini_val) != type(mistral_val):
        differences.append(f"{path}: Типы не совпадают (Gemini: {type(gemini_val).__name__}, Mistral: {type(mistral_val).__name__})")
        return differences
    
    # Сравнение словарей
    if isinstance(gemini_val, dict):
        all_keys = set(gemini_val.keys()) | set(mistral_val.keys())
        for key in sorted(all_keys):
            new_path = f"{path}.{key}" if path else key
            if key not in gemini_val:
                differences.append(f"{new_path}: Отсутствует в Gemini (Mistral: {format_value(mistral_val[key])})")
            elif key not in mistral_val:
                differences.append(f"{new_path}: Отсутствует в Mistral (Gemini: {format_value(gemini_val[key])})")
            else:
                differences.extend(compare_structures(gemini_val[key], mistral_val[key], new_path))
    
    # Сравнение списков
    elif isinstance(gemini_val, list):
        if len(gemini_val) != len(mistral_val):
            differences.append(f"{path}: Разная длина списка (Gemini: {len(gemini_val)}, Mistral: {len(mistral_val)})")
        
        # Детальное сравнение элементов списка
        differences.extend(compare_lists(gemini_val, mistral_val, path))
    
    # Сравнение простых значений
    elif gemini_val != mistral_val:
        differences.append(f"{path}: Значения разные\n  Gemini: {format_value(gemini_val)}\n  Mistral: {format_value(mistral_val)}")
    
    return differences

def load_json_lines(file_path):
    """Загружает файл с несколькими JSON-объектами"""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Ошибка при парсинге строки: {line[:50]}... Ошибка: {str(e)}")
    return data

def compare_results(gemini_file, mistral_file):
    # Загрузка данных
    gemini_data = load_json_lines(gemini_file)
    mistral_data = load_json_lines(mistral_file)

    if not gemini_data:
        print("Ошибка: файл Gemini пуст или содержит некорректные данные")
        return
    if not mistral_data:
        print("Ошибка: файл Mistral пуст или содержит некорректные данные")
        return

    # Берем первый объект Gemini для сравнения
    gemini_first = gemini_data[0]
    
    print("="*80)
    print("Детальное сравнение структур")
    print("="*80)
    
    # Сравниваем с каждым объектом Mistral
    for i, mistral_item in enumerate(mistral_data, 1):
        print(f"\n{'='*30} Сравнение с Mistral объектом #{i} {'='*30}")
        
        # Полное сравнение структур
        all_differences = compare_structures(gemini_first, mistral_item)
        
        if not all_differences:
            print("Структуры полностью идентичны")
            continue
            
        print("\nВсе различия:")
        for diff in all_differences:
            print(f"\n{diff}")

    # Подсчет ошибок
    with open(mistral_file, 'r', encoding='utf-8') as f:
        errors = sum(1 for line in f if '"error"' in line)
    print(f"\nОбщее количество ошибок в Mistral: {errors}")

# Запуск сравнения
compare_results(
    gemini_file='',
    mistral_file=''
)
