from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.append('/opt/airflow/scripts')
from fetch_stock_data import fetch_stock_data, update_postgres

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def pipeline():
    records = fetch_stock_data()
    update_postgres(records)

with DAG(
    'stock_pipeline',
    default_args=default_args,
    description='Fetch and store stock market data',
    schedule_interval='@hourly',
    start_date=datetime(2025, 12, 2),
    catchup=False,
) as dag:
    run_pipeline = PythonOperator(
        task_id='run_stock_pipeline',
        python_callable=pipeline
    )
