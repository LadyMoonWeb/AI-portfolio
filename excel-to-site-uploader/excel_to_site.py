# excel_to_site.py
import pandas as pd
import json

def excel_to_json(excel_file, json_file):
    df = pd.read_excel(excel_file)
    data = df.to_dict(orient="records")
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"✅ Конвертация завершена! Результат: {json_file}")

if __name__ == "__main__":
    excel_to_json("products.xlsx", "products.json")
