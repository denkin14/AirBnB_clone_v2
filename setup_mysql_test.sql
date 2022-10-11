-- Script to prepare MySQL server for AirBnB_v2

-- Create database 'hbnb_test_db'
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
-- Create user 'hbnb_test'
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
-- Grant all privileges to 'hbnb_test' on 'hbnb_test_db' database
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
-- Grant select privileges to 'hbnb_test' on 'performance schema' database
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
