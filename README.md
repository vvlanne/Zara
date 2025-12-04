# ZARA project

## Website description

This project scrapes product data from the "Women Dresses" section of the Zara Kazakhstan website. It collects details about dresses, such as product name, price, and URL.

**URL**:(https://www.zara.com/kz/ru/zhenshchiny-platya-l1066.html?v1=2420896)

## How to run Scraping

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install
4. Run the scraper:
   ```bash
   python3 src/scraper.py

## How to run Airflow

1. Start the Airflow web server and scheduler in separate terminals:
   ```bash
   airflow webserver --port 8080
   airflow scheduler

2. Access Airflow UI at http://localhost:8080
3. Trigger the project DAG manually

## Expected output
1.data/raw_zara_products.csv: Contains raw data scraped from the website.
<img width="1230" height="793" alt="Снимок экрана 2025-12-04 в 23 25 48" src="https://github.com/user-attachments/assets/ac78813c-b3b7-4357-859f-8e40ca8f76eb" />

2. data/clean_zara_products.csv: Contains cleaned and normalized data.
<img width="1246" height="790" alt="Снимок экрана 2025-12-04 в 23 26 36" src="https://github.com/user-attachments/assets/f51c47bf-04de-4470-9888-dcae8254e1f0" />

3. data/output.db: Contains the final cleaned data loaded into an SQLite database.
<img width="1323" height="715" alt="Снимок экрана 2025-12-04 в 23 23 49" src="https://github.com/user-attachments/assets/7cb78943-bb68-4bb8-bf10-a4e6d6b473b8" />

4. UI Airflow
<img width="1436" height="853" alt="Снимок экрана 2025-12-04 в 23 28 14" src="https://github.com/user-attachments/assets/602f99f2-0e89-4726-a620-e6e018078691" />
<img width="749" height="520" alt="Снимок экрана 2025-12-04 в 23 37 10" src="https://github.com/user-attachments/assets/dfe04da8-005a-418b-b6f6-5021ebc97058" />
