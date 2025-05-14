import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://metalworkind.com"

def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def get_base_links():
    url = "https://metalworkind.com/ru/marochnik/rf/poroshkovaya-metallurgiya/"
    soup = get_soup(url)
    
    base_links = []
    ol = soup.find('ol', class_='list-group list-group-numbered')
    if ol:
        for li in ol.find_all('li', class_='list-group-item'):
            a = li.find('a')
            if a and 'href' in a.attrs:
                full_url = urljoin(BASE_URL, a['href'])
                base_links.append(full_url)
    return base_links

def get_pages_links(base_url):
    soup = get_soup(base_url)
    pages_links = []
    
    table = soup.find('div', class_='table-responsive')
    if table:
        for a in table.find_all('a', href=True):
            full_url = urljoin(BASE_URL, a['href'])
            pages_links.append(full_url)
    return pages_links

def parse_page(page_url):
    soup = get_soup(page_url)
    material_card = soup.find('div', class_='material-card')
    
    if not material_card:
        return ""
    
    # Удаляем ненужные элементы (реклама, скрипты)
    for div in material_card.find_all('div', id=lambda x: x and x.startswith('yandex_rtb_')):
        div.decompose()
    for script in material_card.find_all('script'):
        script.decompose()
    
    # Получаем чистый текст и объединяем в одну строку
    text = ' '.join(material_card.stripped_strings)
    return text.replace('\n', ' ').replace('\r', '').replace('\t', ' ')

def get_descriptions():
    try:
        # Получаем базовые ссылки
        base_links = get_base_links()
        print(f"Найдено {len(base_links)} категорий")
        
        all_pages_data = []
        
        # Для каждой базовой ссылки получаем страницы
        for base_link in base_links:
            pages_links = get_pages_links(base_link)
            print(f"Обрабатывается {base_link}, найдено {len(pages_links)} материалов")
            
            # Парсим каждую страницу
            for page_link in pages_links[:5]:
                try:
                    page_data = parse_page(page_link)
                    if page_data:
                        all_pages_data.append(page_data)
                        print(f"Обработана страница: {page_link}")
                except Exception as e:
                    print(f"Ошибка при обработке страницы {page_link}: {e}")
        
        # Сохраняем результаты в файл
        result = ''
        for data in all_pages_data:
            result+=data+'\n'
        
        print(f"Готово! Сохранено {len(all_pages_data)} материалов.")
        return result
    
    except Exception as e:
        print(f"Произошла ошибка: {e}")
