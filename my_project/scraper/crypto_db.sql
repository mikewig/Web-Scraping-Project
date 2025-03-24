CREATE DATABASE IF NOT EXISTS cryptodb;

USE cryptodb;

CREATE TABLE IF NOT EXISTS cryptocurrencies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    symbol VARCHAR(20) UNIQUE
);

CREATE TABLE IF NOT EXISTS price_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    crypto_id INT,
    price FLOAT,
    timestamp DATETIME,
    FOREIGN KEY (crypto_id) REFERENCES cryptocurrencies (id)
);