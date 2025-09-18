# telegram_price_alert.py

import requests
from bs4 import BeautifulSoup
import json
import sys

def parse_products(url):
    """
    Парсит веб-страницу для извлечения информации о товарах.

    Аргументы:
        url (str): URL-адрес страницы для парсинга.

    Возвращает:
        str: JSON-строка со списком словарей, где каждый словарь представляет товар
             с ключами 'title' и 'link'.
             В случае ошибки возвращает JSON с ключом 'error'.
    """
    try:
        # --------------------------------------------------------------------------
        # ШАГ 1: ВЫПОЛНЕНИЕ ЗАПРОСА
        # --------------------------------------------------------------------------
        # Отправляем GET-запрос с заголовками, чтобы имитировать браузер
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()  # Проверяем, успешен ли запрос (код 200)

        # --------------------------------------------------------------------------
        # ШАГ 2: ПАРСИНГ HTML
        # --------------------------------------------------------------------------
        # Используем BeautifulSoup для анализа HTML-содержимого
        soup = BeautifulSoup(response.text, 'html.parser')

        # --------------------------------------------------------------------------
        # ШАГ 3: АДАПТАЦИЯ СЕЛЕКТОРОВ (ВАЖНО!)
        #
        # Замените эти селекторы на актуальные для вашего сайта.
        # Чтобы найти их: откройте сайт -> F12 -> Инспектор -> ПКМ на элементе -> Copy -> Copy selector.
        #
        # Пример для сайта условного магазина:
        # product_selector = "div.product-card"  # Главный блок одного товара
        # title_selector = "a.product-card__title"  # Название товара
        # link_selector = "a.product-card__title"    # Ссылка на товар
        # --------------------------------------------------------------------------
        product_selector = "div.product-item"  # <--- ЗАМЕНИТЬ НА ВАШ СЕЛЕКТОР
        title_selector = "span.product-title"  # <--- ЗАМЕНИТЬ НА ВАШ СЕЛЕКТОР
        link_selector = "a.product-link"       # <--- ЗАМЕНИТЬ НА ВАШ СЕЛЕКТОР

        products = []
        # Находим все блоки товаров на странице
        product_blocks = soup.select(product_selector)

        # Если блоки не найдены, возвращаем ошибку
        if not product_blocks:
            return json.dumps({"error": "Не удалось найти товары по селектору. Проверьте 'product_selector'."})
            
        base_url = new_url.scheme + "://" + new_url.netloc

        for item in product_blocks:
            # Извлекаем название товара
            title_element = item.select_one(title_selector)
            title = title_element.text.strip() if title_element else "Название не найдено"

            # Извлекаем ссылку на товар
            link_element = item.select_one(link_selector)
            
            if link_element and link_element.has_attr('href'):
                 # Собираем абсолютную ссылку, если она относительная
                 href = link_element['href']
                 link = requests.compat.urljoin(base_url, href)
            else:
                 link = "Ссылка не найдена"


            # Добавляем товар в список, если у него есть и название, и ссылка
            if title != "Название не найдено" and link != "Ссылка не найдена":
                products.append({
                    "title": title,
                    "link": link
                })

        return json.dumps(products, ensure_ascii=False)

    except requests.RequestException as e:
        return json.dumps({"error": f"Ошибка сети: {e}"})
    except Exception as e:
        return json.dumps({"error": f"Непредвиденная ошибка: {e}"})

if __name__ == "__main__":
    # Этот блок выполняется, когда скрипт запускается напрямую.
    # Он принимает URL как первый аргумент командной строки.
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
        new_url = requests.utils.urlparse(target_url)
        result = parse_products(target_url)
        print(result)
    else:
        # Сообщение, если URL не был передан
        print(json.dumps({"error": "URL не был передан в качестве аргумента."}))
