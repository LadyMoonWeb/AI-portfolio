# 📦 Excel to Site Uploader

## 🚀 Описание
Скрипт и workflow для **автоматической загрузки товаров из Excel-файла** на сайт через API.  
Идеально подходит для e-commerce: экономит время и исключает ручной ввод карточек.

---

## 🛠 Технологии
- Python (Pandas, Requests)
- n8n (workflow-автоматизация)

---

## 📂 Структура
- `excel_to_site.py` — основной Python-скрипт
- `products.xlsx` — пример входных данных
- `n8n_workflow.json` — схема для n8n
- `requirements.txt` — зависимости Python

---

## 📊 Пример входных данных (`products.xlsx`)
| Name       | Price | Description           |
|------------|-------|-----------------------|
| Product 1  | 100   | Test description...   |
| Product 2  | 200   | Another description.. |

---

## ▶ Как запустить Python-скрипт

1. Установить зависимости:
```bash
pip install -r requirements.txt
2. Запустить загрузку:

python excel_to_site.py

⚙️ Как использовать n8n Workflow

Импортировать n8n_workflow.json в n8n

Указать:

путь к Excel-файлу

API-адрес вашего сайта

Запустить workflow → товары загрузятся автоматически.

📌 Примечания

Поддерживает любой Excel-файл с колонками Name | Price | Description.

API-запросы можно адаптировать под свой e-commerce движок (WooCommerce, OpenCart, Custom API).




