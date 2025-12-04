import os
import sqlite3
from datetime import datetime
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

CLEAN_CSV_PATH = os.path.join(DATA_DIR, "clean_zara_products.csv")
DB_PATH = os.path.join(DATA_DIR, "output.db")


TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS zara_dresses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    price_value REAL NOT NULL,
    price_raw TEXT,
    currency TEXT,
    product_url TEXT,
    scraped_at TEXT
);
"""


def run_loader():
    if not os.path.exists(CLEAN_CSV_PATH):
        raise FileNotFoundError(f"Wasn't found CSV: {CLEAN_CSV_PATH}")

    df = pd.read_csv(CLEAN_CSV_PATH)

    if df.empty:
        raise ValueError("Error")

    os.makedirs(DATA_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(TABLE_SCHEMA)
    conn.commit()


    if "scraped_at" not in df.columns:
        df["scraped_at"] = datetime.utcnow().isoformat(timespec="seconds")

    df_to_insert = df[
        [
            "product_name",
            "price_value",
            "price_raw",
            "currency",
            "product_url",
            "scraped_at",
        ]
    ]

    df_to_insert.to_sql(
        "zara_dresses",
        conn,
        if_exists="append",
        index=False
    )

    conn.commit()
    conn.close()

    print(f"Loaded: {len(df_to_insert)} into zara_dresses → {DB_PATH}")


if __name__ == "__main__":
    run_loader()
