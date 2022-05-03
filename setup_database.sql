CREATE TABLE Sensor
(
    sensor_id INT NOT NULL PRIMARY KEY,
    sensor_name NVARCHAR(20) NOT NULL,
    descriptions TEXT
);

CREATE TABLE Sensor_value
(
    sensor_id INT NOT NULL,
    sensor_value FLOAT NOT NULL,
    measure TEXT,
    time_stamp TEXT,
    FOREIGN KEY (sensor_id) REFERENCES Sensor(sensor_id)
);