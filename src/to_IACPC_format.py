import json
import consts

def transform_data(input_data):
    # Создаем базовую структуру выходного файла
    output_data = {
        "title": consts.NAME_METAL_POWDER_BD,
        "code": "4640008237959055854",
        "path": consts.PATH_TO_METAL_POWDER + consts.NAME_METAL_POWDER_BD + "$;",
        "date": "23.04.2025-20:55:18.103",
        "creation": "23.04.2025-20:55:18.103",
        "owner_id": 746,
        "json_type": "universal",
        "ontology": consts.PATH_TO_METAL_POWDER + consts.NAME_METAL_POWDER_ONTOLOGY + "$;",
        "id": 352303282388996,
        "name": "Наша база металлопорошковых материалов",
        "type": "КОРЕНЬ",
        "meta": "Онтология базы металлопорошковых материалов",
        "successors": [
            {
                "id": 111274012704776,
                "name": "Металлопорошковые материалы",
                "type": "НЕТЕРМИНАЛ",
                "meta": "Класс металлических порошков",
                "successors": []
            }
        ]
    }
    
    materials = output_data["successors"][0]["successors"]
    powder_id = 1112454342  # Начальный ID для порошков
    component_id = 111274012705976  # Начальный ID для компонентов
    
    # База химических элементов для формирования ссылок
    element_base_path = consts.PATH_TO_METAL_POWDER + "База химических элементов$"
    
    # Словарь соответствия русских названий элементов и их символов
    element_names = {
        "Олово": "Sn",
        "Железо": "Fe",
        "Углерод": "C",
        "Кремний": "Si",
        "Марганец": "Mn",
        "Сера": "S",
        "Фосфор": "P",
        "Хром": "Cr",
        "Молибден": "Mo",
        "Никель": "Ni",
        "Медь": "Cu",
        "Алюминий": "Al",
        "Магний": "Mg",
        "Цинк": "Zn",
        "Титан": "Ti",
        "Вольфрам": "W",
        "Кислород": "O",
        "Азот": "N",
        "Водород": "H",
        "Мышьяк": "As",
        "Свинец": "Pb",
        "Сурьма": "Sb",
        "Висмут": "Bi",
        "Кобальт": "Co",
        "Кадмий": "Cd",
        "Самарий": "Sm"
    }

    symbol_to_name = {v: k for k, v in element_names.items()}

    for item in input_data:
        # Создаем структуру для материала
        material = {
            "id": str(powder_id),
            "name": item["name"],
            "type": "НЕТЕРМИНАЛ",
            "meta": "Металлический порошок",
            "successors": [],
            "comment": item.get("comment", "")
        }
        powder_id += 1
        
        # 1. Элементный состав
        element_composition = {
            "id": component_id,
            "name": "Элементный состав",
            "type": "НЕТЕРМИНАЛ",
            "meta": "Элементный состав",
            "successors": []
        }
        component_id += 4
        
        # Находим химический состав в исходных данных
        chem_composition = next((s for s in item.get("successors", []) 
                               if s.get("name") == "Химический состав"), None)
        
        # Находим основной материал (железо, олово и т.д.)
        main_material = next((s for s in item.get("successors", []) 
                            if s.get("name") == "Материал"), None)
        
        # Создаем список всех компонентов
        all_components = []
        
        # Добавляем химические элементы
        if chem_composition:
            for element in chem_composition.get("successors", []):
                if "name" not in element:
                    continue
                
                # Получаем символ элемента
                element_symbol = element_names.get(element["name"], element["name"])
                
                # Получаем русское название элемента
                element_name = symbol_to_name.get(element_symbol, element["name"])
                
                # Проверяем, есть ли уже такой компонент
                component_exists = False
                for comp in all_components:
                    if comp["symbol"] == element_symbol:
                        component_exists = True
                        break
                
                if not component_exists:
                    all_components.append({
                        "name": element_name,  # Русское название
                        "symbol": element_symbol,  # Символ элемента
                        "meta": element.get("meta", "Химический элемент"),
                        "elements": []
                    })
        
        # Формируем структуру с промежуточным уровнем "Компонент"
        component_counter = 1
        for component in all_components:
            component_node = {
                "id": component_id,
                "name": str(component_counter),
                "type": "НЕТЕРМИНАЛ",
                "meta": "Компонент",
                "successors": []
            }
            component_counter += 1
            component_id += 4
            
            # Формируем ссылку на элемент (полное название + символ)
            original_path = f"{element_base_path}/{component['name']}/{component['symbol']};"
            
            if component["symbol"] == "Ca":
                component["symbol"] = "Sm"
                original_path = f"{element_base_path}/Самарий/Sm;"

            if component["symbol"] == "W":
                component["symbol"] = "V"
                original_path = f"{element_base_path}/Ванадий/V;"

            if component["symbol"] == "Na":
                component["symbol"] = "Nb"
                original_path = f"{element_base_path}/Ниобий/Nb;"

            if component["symbol"] == "K":
                component["symbol"] = "Be"
                original_path = f"{element_base_path}/Бериллий/Be;"

            # Создаем узел для элемента/компонента
            element_node = {
                "id": component_id,
                "name": component["symbol"],
                "type": "НЕТЕРМИНАЛ",
                "meta": "Химический элемент",
                "original": original_path,
                "successors": []
            }
            component_id += 4
            
            # Добавляем значения для элемента (если это химический элемент)
            if chem_composition and component["meta"] != "Основной компонент":
                element_data = next((e for e in chem_composition.get("successors", []) 
                                  if e.get("name") == component["name"]), None)
                if element_data:
                    for value in element_data.get("successors", []):
                        if value.get("type") == "ТЕРМИНАЛ-ЗНАЧЕНИЕ":
                            element_node["successors"].append({
                                "value": value.get("value", ""),
                                "type": "ТЕРМИНАЛ-ЗНАЧЕНИЕ",
                                "valtype": value.get("valtype", "REAL"),
                                "meta": "%"
                            })
            
            component_node["successors"].append(element_node)
            element_composition["successors"].append(component_node)
        
        material["successors"].append(element_composition)
        
        method = {
            "name": "Метод получения",
            "type": "НЕТЕРМИНАЛ",
            "meta": "Метод получения",
            "successors": []
        }
        
        material["successors"].append(method)
        
        granulo = {
            "name": "Гранулометрический состав",
            "type": "НЕТЕРМИНАЛ",
            "meta": "Гранулометрический состав",
            "successors": []
        }
        
        granulo_node = next((s for s in item.get("successors", []) 
                           if s.get("name") == "Гранулометрический состав"), None)
        
        if granulo_node:
            for g in granulo_node.get("successors", []):
                if "name" not in g:
                    continue
                    
                granulo_item = {
                    "name": g["name"],
                    "type": "НЕТЕРМИНАЛ",
                    "meta": g.get("meta", g["name"]),
                    "successors": []
                }
                
                if g["name"] == "Форма частиц":
                    for form in g.get("successors", []):
                        if form.get("name") == "Преобладающая форма частиц":
                            granulo_item["successors"].append({
                                "name": "Преобладающая форма частиц",
                                "type": "НЕТЕРМИНАЛ",
                                "meta": "Преобладающая форма частиц",
                                "successors": []
                            })
                
                granulo["successors"].append(granulo_item)
        
        material["successors"].append(granulo)
        
        tech_properties = {
            "name": "Технологические свойства",
            "type": "НЕТЕРМИНАЛ",
            "meta": "Технологические свойства",
            "successors": []
        }
        
        tech_node = next((s for s in item.get("successors", []) 
                         if s.get("name") == "Технологические свойства"), None)
        
        if tech_node:
            for prop in tech_node.get("successors", []):
                if "name" not in prop:
                    continue
                    
                if prop["name"] == "Насыпная плотность":
                    density = {
                        "name": "Насыпная плотность",
                        "type": "НЕТЕРМИНАЛ",
                        "meta": "Насыпная плотность",
                        "successors": []
                    }
                    
                    for d in prop.get("successors", []):
                        if "name" in d and d["name"] == "Числовой интервал":
                            interval = {
                                "name": "Числовой интервал",
                                "type": "НЕТЕРМИНАЛ",
                                "meta": "Числовой интервал",
                                "successors": []
                            }
                            
                            for bound in d.get("successors", []):
                                if "name" in bound and bound["name"] in ["Нижняя граница", "Верхняя граница"]:
                                    bound_node = {
                                        "name": bound["name"],
                                        "type": "НЕТЕРМИНАЛ",
                                        "meta": bound["name"],
                                        "successors": []
                                    }
                                    
                                    for val in bound.get("successors", []):
                                        if val.get("type") == "ТЕРМИНАЛ-ЗНАЧЕНИЕ":
                                            bound_node["successors"].append({
                                                "value": val.get("value", ""),
                                                "type": "ТЕРМИНАЛ-ЗНАЧЕНИЕ",
                                                "valtype": val.get("valtype", "REAL"),
                                                "meta": val.get("meta", "Числовое значение")
                                            })
                                    
                                    interval["successors"].append(bound_node)
                            
                            density["successors"].append(interval)
                        
                        elif d.get("type") == "ТЕРМИНАЛ-ЗНАЧЕНИЕ":
                            density["successors"].append({
                                "value": d.get("value", ""),
                                "type": "ТЕРМИНАЛ-ЗНАЧЕНИЕ",
                                "valtype": d.get("valtype", "STRING"),
                                "meta": "г/см³"
                            })
                    
                    tech_properties["successors"].append(density)
                
                elif prop["name"] == "Сыпучесть":
                    tech_properties["successors"].append({
                        "name": "Сыпучесть",
                        "type": "НЕТЕРМИНАЛ",
                        "meta": "Сыпучесть",
                        "successors": []
                    })
        
        material["successors"].append(tech_properties)
        materials.append(material)
    
    return output_data

with open('output.txt', 'r', encoding='utf-8') as f:
    input_data = [json.loads(line) for line in f]

output_data = transform_data(input_data)

with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print("Преобразование завершено. Результат сохранен в output.json")
