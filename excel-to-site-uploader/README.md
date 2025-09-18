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

---

## 5) Что дальше / короткая инструкция для загрузки в GitHub
1. В твоём репозитории (AI-portfolio) создай папку `excel-to-site-uploader`.
2. Для каждого файла нажми **Add file → Create new file**, вставь имя файла и содержимое (из блоков выше), Commit.
   - ИЛИ локально: создай папку, положи файлы, затем `git add .` → `git commit -m "Add excel-to-site uploader"` → `git push`.
3. Обнови главный `README.md` (корня репо), добавив ссылку на `./excel-to-site-uploader`.

---

Если хочешь — могу прямо сейчас:
- Сгенерировать аналогичные готовые файлы для остальных 4 проектов (price_updater, ai_product_descriptions, telegram_price_alert, faq_chatbot) в таком же полном виде (скрипты + README + n8n JSON).  
Скажи «Да, сгенерируй остальные 4» — и я выдам все файлы сразу, чтобы ты просто скопировала/вставила в соответствующие папки.
