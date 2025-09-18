import pandas as pd
import requests

# Конфигурация API
API_URL = "https://example.com/api/products"  # поменяй на реальный
API_KEY = "your_api_key_here"

# Загружаем данные из Excel
df = pd.read_excel("products.xlsx")

# Отправляем товары на сайт
for _, row in df.iterrows():
    product_data = {
        "name": row["Name"],
        "price": row["Price"],
        "description": row["Description"]
    }

    response = requests.post(
        API_URL,
        json=product_data,
        headers={"Authorization": f"Bearer {API_KEY}"}
    )

    if response.status_code == 201:
        print(f"✅ {row['Name']} успешно загружен")
    else:
        print(f"❌ Ошибка при загрузке {row['Name']}: {response.text}")
