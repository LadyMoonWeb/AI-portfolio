import pandas as pd
import requests

# --- НАСТРОЙКИ: ИЗМЕНИТЕ ЭТИ ЗНАЧЕНИЯ ---
API_ENDPOINT = "https://api.your-store.com/products"  # URL для обновления товара
API_KEY = "your_secret_api_key_here"  # Ваш секретный ключ API
DATA_FILE = "new_prices.xlsx" # Имя вашего Excel-файла
# -----------------------------------------

def update_prices():
    """Главная функция для чтения файла и обновления цен."""
    try:
        # Читаем данные из Excel-файла
        df = pd.read_excel(DATA_FILE)
        print(f"INFO: Загружено {len(df)} строк из файла '{DATA_FILE}'.")
    except FileNotFoundError:
        print(f"ОШИБКА: Файл '{DATA_FILE}' не найден. Убедитесь, что он лежит в той же папке.")
        return
    except Exception as e:
        print(f"ОШИБКА: Не удалось прочитать Excel-файл. Причина: {e}")
        return

    # Готовим заголовки для аутентификации
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    success_count = 0
    failure_count = 0

    # Проходим по каждой строке в файле
    for index, row in df.iterrows():
        sku = row.get('sku')
        price = row.get('new_price')

        if not sku or pd.isna(price):
            print(f"ПРЕДУПРЕЖДЕНИЕ: Пропускаем строку {index + 2}, так как SKU или цена пустые.")
            failure_count += 1
            continue
            
        # Формируем URL для конкретного товара
        url = f"{API_ENDPOINT}/{sku}"
        payload = {"price": float(price)}

        try:
            # Отправляем PUT-запрос для обновления
            response = requests.put(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print(f"УСПЕХ: Цена для SKU {sku} обновлена на {price}.")
                success_count += 1
            else:
                print(f"НЕУДАЧА: SKU {sku}. Сервер ответил: {response.status_code} {response.text}")
                failure_count += 1

        except requests.exceptions.RequestException as e:
            print(f"ОШИБКА СЕТИ: Не удалось обновить SKU {sku}. Причина: {e}")
            failure_count += 1
    
    print("\n--- Отчет ---")
    print(f"Успешно обновлено: {success_count}")
    print(f"Не удалось обновить: {failure_count}")
    print("-------------")

if __name__ == "__main__":
    update_prices()
