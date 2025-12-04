from datetime import datetime, timedelta
import os
import sys

from airflow import DAG
from airflow.operators.python import PythonOperator

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")

if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from scraper import run_scraper
from cleaner import run_cleaner
from loader import run_loader


default_args = {
    "owner": "data_pipeline",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="zara_dresses_pipeline",
    default_args=default_args,
    description="Zara dresses: scrape → clean → load to SQLite",
    schedule_interval="@daily",  
    start_date=datetime(2025, 12, 1),
    catchup=False,
    max_active_runs=1,
) as dag:

    scrape_task = PythonOperator(
        task_id="scrape_zara_dresses",
        python_callable=run_scraper,
    )

    clean_task = PythonOperator(
        task_id="clean_zara_dresses",
        python_callable=run_cleaner,
    )

    load_task = PythonOperator(
        task_id="load_zara_dresses_to_sqlite",
        python_callable=run_loader,
    )

    scrape_task >> clean_task >> load_task
