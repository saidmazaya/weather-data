FROM apache/airflow:2.7.1

# Install dependencies
RUN pip install psycopg2-binary requests pendulum apache-airflow
