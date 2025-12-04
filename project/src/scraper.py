import os
from datetime import datetime
from urllib.parse import urljoin

import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

CATEGORY_URL = "https://www.zara.com/kz/ru/zhenshchiny-platya-l1066.html?v1=2420896"
BASE_URL = "https://www.zara.com"

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

RAW_CSV_PATH = os.path.join(DATA_DIR, "raw_zara_products.csv")


def deep_scroll(page, attempts=120):
    last_height = 0
    for _ in range(attempts):
        page.mouse.wheel(0, 6000)
        page.wait_for_timeout(600)
        new_height = page.evaluate("document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def extract_products_from_html(html: str):
    soup = BeautifulSoup(html, "html.parser")
    texts = [t.strip() for t in soup.stripped_strings]

    products = []
    seen = set()

    KEYWORDS = ["ПЛАТЬЕ"]

    def is_name(txt: str):
        return any(k in txt.upper() for k in KEYWORDS)

    def find_price_after(i):
        for j in range(i + 1, min(i + 20, len(texts))):
            t = texts[j]
            if t.startswith("T ") and any(ch.isdigit() for ch in t):
                return t
        return None


    name_to_url = {}
    for a in soup.find_all("a"):
        text = a.get_text(strip=True) or ""
        href = a.get("href")
        if text and href:
            name_to_url[text] = urljoin(BASE_URL, href)


    for i, txt in enumerate(texts):
        if not is_name(txt):
            continue

        price = find_price_after(i)
        if not price:
            continue

        if (txt, price) in seen:
            continue
        seen.add((txt, price))

        url = name_to_url.get(txt, "")
        if not url:
            a = soup.find("a", string=lambda s: s and txt in s)
            if a and a.get("href"):
                url = urljoin(BASE_URL, a.get("href"))

        products.append({
            "product_name": txt,
            "price_raw": price,
            "product_url": url,
            "scraped_at": datetime.utcnow().isoformat(timespec="seconds"),
        })

    return products


def run_scraper():
    all_products = []

    with sync_playwright() as p:
        browser = p.webkit.launch(headless=False)

        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
            ),
            locale="ru-RU",
            viewport={"width": 1400, "height": 950},
        )

        page = context.new_page()

        print(f"\nCollecting:")
        page.goto(CATEGORY_URL, wait_until="networkidle", timeout=200_000)

        deep_scroll(page, attempts=120)

        html = page.content()
        products = extract_products_from_html(html)

        print(f"Found: {len(products)}")
        all_products.extend(products)

        browser.close()

    df = pd.DataFrame(all_products)
    df.to_csv(RAW_CSV_PATH, index=False, encoding="utf-8")

    print(f"\nDone: {len(df)} saved {RAW_CSV_PATH}")
    return df


if __name__ == "__main__":
    run_scraper()
