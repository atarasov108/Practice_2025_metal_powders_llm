from transformers import AutoModelForCausalLM, AutoTokenizer
import json

model_name = "HuggingFaceH4/zephyr-7b-beta"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="cpu")  # Изменено здесь

from consts import PROMPT

def get_json_mistral(description: str) -> str:
    prompt = PROMPT + description
    inputs = tokenizer(prompt, return_tensors="pt").to("cpu")  # Добавлено .to("cpu")
    outputs = model.generate(**inputs, max_new_tokens=1000)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    try:
        start_idx = response.find("{")
        end_idx = response.rfind("}") + 1
        json_str = response[start_idx:end_idx]
        json.loads(json_str)
        return json_str
    except:
        return '{"error": "Failed to parse JSON"}'

# Пример данных (аналогичные данным из Gemini)
data = """
ПЖВ1 порошок железный Характеристики материала Марка порошка: ПЖВ1 Классификация: Порошок железный Применение: Порошок получен методом восстановления, предназначен для изготовления изделий методом порошковой металлургии, сварочных материалов и других целей. При давлении 400 МПа плотность не менее 6.4 г/см 3 . При давлении 700 МПа плотность не менее 7.1 г/см 3 (класс крупности 160 и 200) Химические свойства Хим. состав материала Элемент Массовая доля, % C до 0.02 Si до 0.08 Mn до 0.1 S до 0.015 P до 0.15 Источники информации и нормативная документация ГОСТ 9849-86
"""

with open('output_mistral.txt', mode='a') as f:
    for line in data.split('\n'):
        if line.strip():
            r = get_json_mistral(line)
            print(r)
            f.write(r + '\n\n')