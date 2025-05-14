import google.generativeai as genai
from parser_html import get_descriptions
import time
import json
from consts import PROMPT

# Настройка API Gemini
genai.configure(api_key='')# указать ключ gemini api

# Конфигурация модели
model = genai.GenerativeModel(
    "gemini-1.5-flash",
    generation_config={
        "response_mime_type": "application/json",
        "temperature": 0.3  # Для более детерминированных ответов
    }
)

def get_json(description: str) -> str:
    """
    Генерирует JSON структуру на основе описания материала.
    
    Args:
        description (str): Текст с описанием материала
        
    Returns:
        str: JSON строка с извлеченной информацией
    """
    try:
        response = model.generate_content(PROMPT + description)
        # Попробуем проверить валидность JSON
        json.loads(response.text)
        return response.text
    except Exception as e:
        print(f"Ошибка при обработке описания: {e}")
        return json.dumps({"error": str(e)})

def process_descriptions(output_file: str, delay: int = 10):
    """
    Обрабатывает все описания из входного файла и сохраняет результаты.
    
    Args:
        input_file (str): Путь к файлу с исходными описаниями
        output_file (str): Путь к файлу для сохранения результатов
        delay (int): Задержка между запросами в секундах
    """
    descriptions = get_descriptions()
    
    with open(output_file, mode='w', encoding='utf-8') as f:
        for i, desc in enumerate(descriptions.split('\n')):
            if i > 20:
                break
            if not desc.strip():
                continue
                
            print(f"Обработка описания {i+1}...")
            result = get_json(desc)
                
            f.write(result)
            f.write('\n')
            
            print(f"Описание {i+1} обработано и сохранено.")
            time.sleep(delay)

if __name__ == "__main__":
    # Конфигурация обработки
    OUTPUT_FILE = 'output.txt'
    REQUEST_DELAY = 10  # секунд
    
    print("Начало обработки материалов...")
    process_descriptions(OUTPUT_FILE, REQUEST_DELAY)
    print("Обработка завершена. Результаты сохранены в", OUTPUT_FILE)