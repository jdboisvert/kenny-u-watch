CREATE DATABASE IF NOT EXISTS alertproducer;
USE alertproducer;
CREATE TABLE IF NOT EXISTS vehicle (
  id INT PRIMARY KEY AUTO_INCREMENT,
  manufacturer_name VARCHAR(255) NOT NULL,
  model_name VARCHAR(255) NOT NULL,
  model_year VARCHAR(4) NOT NULL,
  last_row_id VARCHAR(16),
  branch_location VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS subscription (
    id INT PRIMARY KEY AUTO_INCREMENT,
    client_id VARCHAR(255) NOT NULL,
    vehicle_id INT NOT NULL,
    FOREIGN KEY (vehicle_id)
        REFERENCES vehicle(id)
        ON DELETE CASCADE,
    UNIQUE KEY unique_per_user (client_id, vehicle_id)
);
