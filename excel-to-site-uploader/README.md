# Excel → Site Uploader

**Краткое:** Скрипт читает `products.xlsx` и выгружает товары на REST API. В репо также есть пример CSV/xlsx и n8n workflow (импортируемый).

## Файлы
- `excel_to_site.py` — основной Python-скрипт
- `create_products_xlsx.py` — скрипт, который создаёт `products.xlsx` с примерами
- `products.csv` — (опционально) пример CSV
- `n8n_workflow.json` — импортируемая схема для n8n (см. инструкции ниже)

## Как протестировать локально
1. Создай `products.xlsx`:
   - Либо открой `products.csv` в Excel и сохрани как `.xlsx`
   - Либо запусти `python create_products_xlsx.py`
2. Настрой `API_URL` и, если нужно, `API_KEY` в `excel_to_site.py`.
3. Установи зависимости:
```bash
pip install pandas openpyxl requests
4. python excel_to_site.py

