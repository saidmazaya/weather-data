from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import datetime, timedelta
import requests
import psycopg2
import pendulum
import os

local_tz = pendulum.timezone("Asia/Jakarta")

default_args = {
    'owner': 'postgres',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'start_date': datetime(2023, 10, 30, tzinfo=local_tz),
    'retries': 5,
    'retry_delay': timedelta(minutes=1)  # Menunggu 1 menit sebelum mencoba eksekusi ulang
}

DB_CONFIG = {
    'host': 'host.docker.internal',
    'port': 5433,
    'database': 'weather_data',
    'user': 'postgres',
    'password': 'postgres',
}

API_KEY = os.environ.get('API_KEY')
API_URL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline'

def get_weather_data_by_day_and_time(day, time, cur):
    # Kode SQL untuk mengambil data berdasarkan hari dan jam
    sql = "SELECT * FROM cuaca_jam_pg WHERE tanggal = %s AND jam = %s"
    val = (day, time)
    cur.execute(sql, val)
    result = cur.fetchone()
    return result

def extract(**kwargs):
    ts = 'today'
    params = {
        'unitGroup': 'metric',
        'include': 'hours',
        'key': API_KEY,
        'contentType': 'json'
    }
    api_url = f"{API_URL}/{kwargs['location']}/{ts}"
    response = requests.get(api_url, params=params)
    raw_data = response.json()

    tanggal_ex = raw_data['days'][0]['datetime']
    jam_ex_list = raw_data['days'][0]['hours']

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    for jam_ex in jam_ex_list:
        jam_datetime = jam_ex['datetime']
        existing_data = get_weather_data_by_day_and_time(tanggal_ex, jam_datetime, cur)

        if existing_data is None:
            kwargs['ti'].xcom_push(key='raw_data', value=raw_data)
        else:
            raise Exception("Data dengan hari dan jam yang sama sudah ada dalam database.")

    conn.close()

# Modify transform task to push a list
def transform(**kwargs):
    raw_data = kwargs['ti'].xcom_pull(key='raw_data', task_ids='extract')
    datetimetes = raw_data['days'][0]['datetime']

    day = raw_data['days'][0]
    hourly_data = day['hours']

    transformed_data = []  # Create an empty list

    for hour in hourly_data:
        data = {
            'tanggal': datetimetes,
            'datetime': hour['datetime'],
            'temp': hour['temp'],
            'feelslike': hour['feelslike'],
            'humidity': hour['humidity'],
            'dew': hour['dew'],
            'windgust': hour['windgust'],
            'windspeed': hour['windspeed'],
            'winddir': hour['winddir'],
            'pressure': hour['pressure'],
            'visibility': hour['visibility'],
            'cloudcover': hour['cloudcover'],
            'solarradiation': hour['solarradiation'],
            'solarenergy': hour['solarenergy'],
            'uvindex': hour['uvindex'],
            'conditions': hour['conditions'],
            'icon': hour['icon'],
            'source': hour['source']
        }
        transformed_data.append(data)  # Append each data dictionary to the list

    kwargs['ti'].xcom_push(key='transformed_data', value=transformed_data)  # Push the list

# Modify load task to handle the list
def load(**kwargs):
    data_list = kwargs['ti'].xcom_pull(key='transformed_data', task_ids='transform')
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    for data in data_list:
        existing_data = get_weather_data_by_day_and_time(data['tanggal'], data['datetime'], cur)

        if existing_data is None:
            sql = """INSERT INTO cuaca_jam_pg (tanggal, jam, temperature, feelslike, humidity, dew_point, wind_gust, wind_speed, wind_direction, pressure, visibility, cloud_cover, solarradiation, solarenergy, uv_index, conditions, icon, source, tanggal_pengambilan, jam_pengambilan)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_DATE, CURRENT_TIME)
                """
            cur.execute(sql, (
                data.get('tanggal'), data.get('datetime'), data.get('temp'), data.get('feelslike'), data.get('humidity'),
                data.get('dew'), data.get('windgust'), data.get('windspeed'), data.get('winddir'), data.get('pressure'),
                data.get('visibility'), data.get('cloudcover'), data.get('solarradiation'), data.get('solarenergy'),
                data.get('uvindex'), data.get('conditions'), data.get('icon'), data.get('source')
            ))
            conn.commit()
    conn.close()
        
with DAG('weather_etl_pg_docker_satu',
         default_args=default_args,
         schedule='0 19 * * *',
         max_active_runs=1,
         catchup= False) as dag:
    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract,
        op_kwargs={'location': 'pennsylvania'}
    )

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform,
    )

    load_task = PythonOperator(
        task_id='load',
        python_callable=load,
    )

extract_task >> transform_task >> load_task
