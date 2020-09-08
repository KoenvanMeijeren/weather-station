-- creates clean database for weather station
DROP USER IF EXISTS 'sensem'@'localhost';
DROP USER IF EXISTS 'senser'@'localhost';
DROP DATABASE IF EXISTS weatherstation;

CREATE DATABASE weatherstation;
USE weatherstation;

CREATE TABLE sensor (
  id INT(11) NOT NULL AUTO_INCREMENT,
  name VARCHAR(45),
  unity VARCHAR(45),
  PRIMARY KEY (id)
);

CREATE TABLE measurement (
  id INT(11) NOT NULL AUTO_INCREMENT,
  sensor_id INT(11) NOT NULL,
  time TIMESTAMP,
  value FLOAT DEFAULT NULL,
  PRIMARY KEY (id),
  KEY fk_measurement_sensor (sensor_id),
  CONSTRAINT fk_measurement_sensor FOREIGN KEY (sensor_id) REFERENCES sensor (id)
);

CREATE USER 'sensem'@'localhost' IDENTIFIED BY 'h@';
CREATE USER 'senser'@'localhost' IDENTIFIED BY 'h@';

GRANT INSERT ON weatherstation.measurement TO 'sensem'@'localhost';
GRANT SELECT ON weatherstation.sensor TO 'sensem'@'localhost';
GRANT SELECT ON weatherstation.* TO 'senser'@'localhost';
