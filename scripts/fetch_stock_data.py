import os
import requests
import psycopg2
import pandas as pd
from datetime import datetime

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
STOCK_SYMBOL = os.getenv("STOCK_SYMBOL")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")

def fetch_stock_data():
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={STOCK_SYMBOL}&interval=60min&apikey={API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        ts = data.get('Time Series (60min)', {})
        if not ts:
            print("No data returned from API.")
            return []

        records = []
        for time, values in ts.items():
            records.append({
                'symbol': STOCK_SYMBOL,
                'timestamp': datetime.strptime(time, '%Y-%m-%d %H:%M:%S'),
                'open': float(values['1. open']),
                'high': float(values['2. high']),
                'low': float(values['3. low']),
                'close': float(values['4. close']),
                'volume': int(values['5. volume'])
            })
        return records
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def update_postgres(records):
    if not records:
        print("No records to insert.")
        return
    try:
        conn = psycopg2.connect(
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST
        )
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS stock_data (
            symbol TEXT,
            timestamp TIMESTAMP PRIMARY KEY,
            open NUMERIC,
            high NUMERIC,
            low NUMERIC,
            close NUMERIC,
            volume BIGINT
        )
        """)
        for r in records:
            cur.execute("""
            INSERT INTO stock_data (symbol, timestamp, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (timestamp) DO NOTHING
            """, (r['symbol'], r['timestamp'], r['open'], r['high'], r['low'], r['close'], r['volume']))
        conn.commit()
        cur.close()
        conn.close()
        print(f"{len(records)} records inserted successfully.")
    except Exception as e:
        print(f"Error updating database: {e}")

if __name__ == "__main__":
    records = fetch_stock_data()
    update_postgres(records)
