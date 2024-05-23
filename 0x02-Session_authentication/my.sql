-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS my_database;

-- Switch to the newly created database
USE my_database;

-- Create the users table
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    created_at DATETIME,
    updated_at DATETIME,
    email VARCHAR(255),
    _password VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255)
);

-- Insert data into the users table
INSERT INTO users (id, created_at, updated_at, email, _password, first_name, last_name)
VALUES (
    '9c85d3db-5e4c-40f5-9629-7269cf42b77e',
    '2024-05-23T18:02:01',
    '2024-05-23T18:02:01',
    'bob@hbtn.io',
    'a5c904771b8617de27d3511d1f538094e26c120da663363b3f760f7b894f9d69',
    NULL,
    NULL
);
