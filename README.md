
# Real Time Hourly Weather Data New York And Pennsylvania

Weather Data Management System Using Docker, Airflow, ETL, MySQL, PostgreSQL, Python




## API Reference

#### Get New York Data

```http
  GET https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/new%20york/today
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `unitGroup` | `string` | Metric or US |
| `include` | `string` | hours |
| `api_key` | `string` | **Required**. Your API key |
| `contentType` | `string` | json |

#### Get Pennsylvania Data

```http
  GET https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/pennsylvania/today
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `unitGroup` | `string` | Metric or US |
| `include` | `string` | hours |
| `api_key` | `string` | **Required**. Your API key |
| `contentType` | `string` | json |



## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`API_KEY`

If you need to change the database configuration you can change it in 

`docker-compose.yaml`




## Run Locally

Clone the project

```bash
  git clone https://github.com/saidmazaya/weather-data.git
```

Go to the project directory

```bash
  cd my-project
```

Install Airflow

```bash
  docker compose up airflow-init
```

Start the Docker and Install dependencies

```bash
  docker compose up --build
```

