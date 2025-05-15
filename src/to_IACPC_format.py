import json
import consts

def transform_data(input_data):
    output_data = {
        "title": consts.NAME_METAL_POWDER_BD,
        "code": "4640008237959055854",
        "path": consts.PATH_TO_METAL_POWDER_BD,
        "date": "23.04.2025-20:55:18.103",
        "creation": "23.04.2025-20:55:18.103",
        "owner_id": 746,
        "json_type": "universal",
        "ontology": consts.PATH_TO_METAL_POWDER_ONTOLOGY,
        "id": 352303282388996,
        "name": consts.NAME_METAL_POWDER_BD,
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
    
    powder_id = 1112454342
    
    for item in input_data:
        material = {
            "id": str(powder_id),
            "name": item["name"],
            "type": "НЕТЕРМИНАЛ",
            "meta": "Металлический порошок",
            "successors": [],
            "comment": item.get("comment", "")
        }
        
        powder_id += 1
        
        element_composition = {
            "name": "Элементный состав",
            "type": "НЕТЕРМИНАЛ",
            "meta": "Элементный состав",
            "successors": []
        }
        
        chem_composition = None
        main_material = None
        for successor in item.get("successors", []):
            if successor.get("name") == "Химический состав":
                chem_composition = successor
            elif successor.get("name") == "Материал":
                main_material = successor
        
        if main_material:
            for mat_successor in main_material.get("successors", []):
                if "name" in mat_successor:
                    element_composition["successors"].append({
                        "name": mat_successor["name"],
                        "type": "НЕТЕРМИНАЛ",
                        "meta": "Компонент",
                        "successors": []
                    })
        
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
        
        for successor in item.get("successors", []):
            if successor.get("name") == "Гранулометрический состав":
                for granulo_successor in successor.get("successors", []):
                    if "name" in granulo_successor and granulo_successor["name"] in ["Размер частиц", "Форма частиц"]:
                        new_granulo = {
                            "name": granulo_successor["name"],
                            "type": "НЕТЕРМИНАЛ",
                            "meta": granulo_successor["name"],
                            "successors": []
                        }
                        
                        if granulo_successor["name"] == "Форма частиц":
                            for form_successor in granulo_successor.get("successors", []):
                                if "name" in form_successor and form_successor["name"] == "Преобладающая форма частиц":
                                    new_granulo["successors"].append({
                                        "name": "Преобладающая форма частиц",
                                        "type": "НЕТЕРМИНАЛ",
                                        "meta": "Преобладающая форма частиц",
                                        "successors": []
                                    })
                        
                        granulo["successors"].append(new_granulo)
        
        material["successors"].append(granulo)
        
        tech_properties = {
            "name": "Технологические свойства",
            "type": "НЕТЕРМИНАЛ",
            "meta": "Технологические свойства",
            "successors": []
        }
        
        for successor in item.get("successors", []):
            if successor.get("name") == "Технологические свойства":
                for tech_successor in successor.get("successors", []):
                    if "name" not in tech_successor:
                        continue
                        
                    if tech_successor["name"] == "Насыпная плотность":
                        density = {
                            "name": "Насыпная плотность",
                            "type": "НЕТЕРМИНАЛ",
                            "meta": "Насыпная плотность",
                            "successors": []
                        }
                        
                        for density_successor in tech_successor.get("successors", []):
                            if "name" in density_successor and density_successor["name"] == "Числовой интервал":
                                interval = {
                                    "name": "Числовой интервал",
                                    "type": "НЕТЕРМИНАЛ",
                                    "meta": "Числовой интервал",
                                    "successors": []
                                }
                                
                                for interval_successor in density_successor.get("successors", []):
                                    if "name" in interval_successor and interval_successor["name"] in ["Нижняя граница", "Верхняя граница"]:
                                        bound = {
                                            "name": interval_successor["name"],
                                            "type": "НЕТЕРМИНАЛ",
                                            "meta": interval_successor["name"],
                                            "successors": []
                                        }
                                        
                                        for bound_successor in interval_successor.get("successors", []):
                                            if bound_successor.get("type") == "ТЕРМИНАЛ-ЗНАЧЕНИЕ":
                                                bound["successors"].append({
                                                    "value": bound_successor.get("value", ""),
                                                    "type": "ТЕРМИНАЛ-ЗНАЧЕНИЕ",
                                                    "valtype": bound_successor.get("valtype", "REAL"),
                                                    "meta": "Числовое значение"
                                                })
                                        
                                        interval["successors"].append(bound)
                                
                                density["successors"].append(interval)
                            
                            elif density_successor.get("type") == "ТЕРМИНАЛ-ЗНАЧЕНИЕ" and density_successor.get("meta") in ["г/см³", "Единицы измерения"]:
                                density["successors"].append({
                                    "value": density_successor.get("value", ""),
                                    "type": "ТЕРМИНАЛ-ЗНАЧЕНИЕ",
                                    "valtype": density_successor.get("valtype", "STRING"),
                                    "meta": "г/см³"
                                })
                        
                        tech_properties["successors"].append(density)
                    
                    elif tech_successor["name"] == "Сыпучесть":
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
