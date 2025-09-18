# excel_to_site.py
import pandas as pd
import requests

EXCEL_FILE = "products.xlsx"
API_URL = "https://demo-site.com/api/products"

df = pd.read_excel(EXCEL_FILE)

for _, row in df.iterrows():
    payload = {
        "name": row["Name"],
        "price": row["Price"],
        "description": row["Description"]
    }
    r = requests.post(API_URL, json=payload)
    print(f"{row['Name']} → {r.status_code}")
