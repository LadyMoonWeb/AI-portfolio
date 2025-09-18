# 📦 Excel to Site Uploader

**Описание:**  
Скрипт загружает товары из Excel-файла напрямую на сайт (через API).  
Идеально подходит для e-commerce, чтобы не вбивать карточки вручную.

**Технологии:** Python, Pandas, Requests

**Файлы:**
- `excel_to_site.py` — основной скрипт
- `products.xlsx` — пример входных данных
- `n8n_workflow.json` — схема для n8n

**Пример входных данных:**
| Name         | Price | Description             |
|-------------|------|-----------------------|
| Product 1   | 100  | Test description...   |
| Product 2   | 200  | Another description.. |

**Как запустить:**
```bash
pip install pandas requests
python excel_to_site.py
