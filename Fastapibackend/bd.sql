CREATE DATABASE traveldb;

USE traveldb;

CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    destination VARCHAR(255),
    date DATE,
    type VARCHAR(50)
);
