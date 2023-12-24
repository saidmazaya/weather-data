SET TIME ZONE 'Asia/Jakarta';

-- Database: weather_data

-- DROP DATABASE IF EXISTS weather_data;

CREATE DATABASE weather_data;  
-- Table: public.cuaca_jam

-- DROP TABLE IF EXISTS public.cuaca_jam;
\c weather_data;
CREATE TABLE IF NOT EXISTS public.cuaca_jam_pg
(
    id SERIAL NOT NULL,
    tanggal date,
    jam time without time zone,
    temperature numeric(5,2),
    feelslike numeric(5,2),
    humidity numeric(5,2),
    dew_point numeric(5,2),
    wind_gust numeric(5,2),
    wind_speed numeric(5,2),
    wind_direction numeric(5,2),
    pressure numeric(6,2),
    visibility numeric(5,2),
    cloud_cover numeric(5,2),
    solarradiation numeric(5,2),
    solarenergy numeric(5,2),
    uv_index numeric(3,1),
    conditions character varying(100) COLLATE pg_catalog."default",
    icon character varying(100) COLLATE pg_catalog."default",
    source character varying(100) COLLATE pg_catalog."default",
    tanggal_pengambilan date DEFAULT now(),
    jam_pengambilan time(0) without time zone DEFAULT now(),
    city character varying(100) COLLATE pg_catalog."default" DEFAULT 'Pennsylvania'::character varying,
    CONSTRAINT cuaca_jam_pkey PRIMARY KEY (id)
)

-- ALTER TABLE IF EXISTS public.cuaca_jam
--     OWNER to postgres;
