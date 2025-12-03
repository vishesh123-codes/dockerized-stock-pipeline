# Dockerized Stock Market Data Pipeline

This project is a Dockerized Data Pipeline built using Airflow that fetches stock market data from a free API, processes it, and stores it in PostgreSQL. The pipeline is fully containerized and can be run using Docker Compose.

## Features
- Fetch stock data from API (JSON format)
- Process and clean data
- Store data in PostgreSQL
- Fully containerized using Docker Compose
- Scheduled DAGs (Airflow) to run hourly/daily

## Requirements
- Docker & Docker Compose installed

## Setup & Run

1. **Clone the repository**
```bash
git clone https://github.com/vishesh123-codes/dockerized-stock-pipeline.git
cd dockerized-stock-pipeline


Set environment variables (PostgreSQL)

POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_DB=airflow


Start Docker containers

docker-compose up -d


Access Airflow

Open browser: http://localhost:8080

Login credentials:

Username: admin

Password: admin

Enable DAG

Left sidebar → DAGs → stock_pipeline → toggle ON

Trigger DAG manually (optional) to test

