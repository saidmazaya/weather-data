SET time_zone = "+07:00";
CREATE DATABASE IF NOT EXISTS weather_data;
USE weather_data;

CREATE TABLE `cuaca_jam` (
  `id` int(11) NOT NULL,
  `tanggal` date DEFAULT NULL,
  `jam` time DEFAULT NULL,
  `temperature` float(5,2) DEFAULT NULL,
  `feelslike` float(5,2) DEFAULT NULL,
  `humidity` float(5,2) DEFAULT NULL,
  `dew_point` float(5,2) DEFAULT NULL,
  `wind_gust` float(5,2) DEFAULT NULL,
  `wind_speed` float(5,2) DEFAULT NULL,
  `wind_direction` float(5,2) DEFAULT NULL,
  `pressure` float(6,2) DEFAULT NULL,
  `visibility` float(5,2) DEFAULT NULL,
  `cloud_cover` float(5,2) DEFAULT NULL,
  `solarradiation` float(5,2) DEFAULT NULL,
  `solarenergy` float(5,2) DEFAULT NULL,
  `uv_index` float(3,1) DEFAULT NULL,
  `conditions` varchar(100) DEFAULT NULL,
  `icon` varchar(100) DEFAULT NULL,
  `source` varchar(100) DEFAULT NULL,
  `tanggal_pengambilan` date DEFAULT NULL,
  `jam_pengambilan` time DEFAULT NULL,
  `city` varchar(100) DEFAULT 'New York'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `cuaca_jam`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `cuaca_jam`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;