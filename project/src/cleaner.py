import os
import re
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

RAW_CSV_PATH = os.path.join(DATA_DIR, "raw_zara_products.csv")
CLEAN_CSV_PATH = os.path.join(DATA_DIR, "clean_zara_products.csv")


def parse_price(price_raw: str):
    if not isinstance(price_raw, str):
        return None, None

    txt = price_raw.strip()

    currency = None
    if txt.startswith("T"):
        currency = "KZT"
        txt = txt[1:].strip()


    cleaned = txt.replace(" ", "").replace("\xa0", "")
    cleaned = cleaned.replace(",", ".")
    cleaned = re.sub(r"[^0-9.]", "", cleaned)

    if not cleaned:
        return None, currency

    try:
        value = float(cleaned)
    except ValueError:
        value = None

    return value, currency


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame()

    df = df.copy()

    df["product_name"] = df["product_name"].astype(str).str.strip()
    df["price_raw"] = df["price_raw"].astype(str).str.strip()
    df["product_url"] = df["product_url"].astype(str).str.strip()


    df = df[(df["product_name"] != "") & (df["price_raw"] != "")]


    parsed = df["price_raw"].apply(parse_price)
    df["price_value"] = parsed.map(lambda x: x[0])
    df["currency"] = parsed.map(lambda x: x[1])


    df = df[df["price_value"].notna()]


    df["product_url"].replace({"": None, "nan": None}, inplace=True)


    df["product_name"] = (
        df["product_name"]
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

 
    df.drop_duplicates(
        subset=["product_name", "price_value", "product_url"],
        inplace=True
    )

    df.reset_index(drop=True, inplace=True)
    return df


def run_cleaner() -> pd.DataFrame:
    if not os.path.exists(RAW_CSV_PATH):
        raise FileNotFoundError(f"Нет файла: {RAW_CSV_PATH}")

    df_raw = pd.read_csv(RAW_CSV_PATH)
    df_clean = clean_dataframe(df_raw)

    df_clean.to_csv(CLEAN_CSV_PATH, index=False, encoding="utf-8")
    print(f"Cleaned: {len(df_clean)}, saved in {CLEAN_CSV_PATH}")

    return df_clean


if __name__ == "__main__":
    run_cleaner()
