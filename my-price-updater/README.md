# 💲 Price Updater Bot: Автоматическое обновление цен

Это простой, но мощный бот для автоматического обновления цен на вашем сайте или в любой другой системе. Он читает новые цены из Excel-файла и отправляет их через API.

Этот проект можно реализовать двумя спосоями:
1.  **Как простой Python-скрипт** (для локального запуска).
2.  **Как workflow в n8n** (для надежной автоматизации в облаке).

---

## 🚀 Как запустить (Python-версия)

1.  **Подготовьте данные:**
    * Положите рядом со скриптом файл `new_prices.xlsx`.
    * В файле должны быть два столбца: `sku` (артикул товара) и `new_price` (новая цена).

2.  **Установите библиотеки:**
    Откройте терминал и выполните команду:
    ```bash
    pip install pandas openpyxl requests
    ```

3.  **Настройте скрипт:**
    * Откройте файл `price_updater.py`.
    * В самом верху найдите и измените `API_ENDPOINT` (URL вашего магазина) и `API_KEY` (ваш секретный ключ).

4.  **Запустите:**
    ```bash
    python price_updater.py
    ```
    Скрипт обработает все строки в Excel и выведет результат в консоль.

---

##  workflow "Как запустить (n8n-версия)"

1.  **Скопируйте JSON-код:**
    Скопируйте весь код из блока ниже.

2.  **Импортируйте в n8n:**
    * В интерфейсе n8n выберите `Import` -> `From Clipboard`.
    * Вставьте скопированный код.

3.  **Настройте узлы (nodes):**
    * **Google Sheets / Read from File:** Укажите, откуда брать файл с ценами.
    * **HTTP Request:** Введите URL вашего API и настройте безопасное хранение ключа через Credentials.
    * **Активируйте workflow.**

<details>
<summary>📌 Нажмите, чтобы развернуть JSON-код для n8n</summary>

```json
{
  "name": "Price Updater Bot",
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [
            {
              "unit": "minutes",
              "number": 15
            }
          ]
        }
      },
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1,
      "position": [
        450,
        300
      ]
    },
    {
      "parameters": {
        "operation": "read",
        "documentId": "YOUR_GOOGLE_SHEET_ID",
        "sheetName": "Sheet1",
        "options": {}
      },
      "name": "Read Prices from Sheet",
      "type": "n8n-nodes-base.googleSheets",
      "typeVersion": 1,
      "position": [
        650,
        300
      ],
      "credentials": {
        "googleSheetsApi": {
          "id": "YOUR_CREDENTIAL_ID",
          "name": "Google Sheets account"
        }
      }
    },
    {
      "parameters": {
        "url": "[https://api.your-store.com/products/](https://api.your-store.com/products/){{$json[\"sku\"]}}",
        "authentication": "headerAuth",
        "options": {},
        "bodyParameters": {
          "parameters": [
            {
              "name": "price",
              "value": "={{$json[\"new_price\"]}}"
            }
          ]
        }
      },
      "name": "Update Price via API",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 1,
      "position": [
        850,
        300
      ],
      "credentials": {
        "httpHeaderAuth": {
          "id": "YOUR_API_KEY_CREDENTIAL_ID",
          "name": "Store API Key"
        }
      }
    }
  ],
  "connections": {
    "Schedule Trigger": {
      "main": [
        [
          {
            "node": "Read Prices from Sheet",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Read Prices from Sheet": {
      "main": [
        [
          {
            "node": "Update Price via API",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```
</details>

---

## 🛠️ Технологии

* **Python:** Pandas, Requests
* **Автоматизация:** n8n.io
* **Данные:** Microsoft Excel
