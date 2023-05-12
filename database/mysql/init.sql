CREATE USER 'auth_user' @'%' IDENTIFIED BY 'Auth1234';
DROP DATABASE if EXISTS auth;
CREATE DATABASE auth;
GRANT ALL PRIVILEGES ON auth.* TO 'auth_user' @'%';
USE auth;
DROP TABLE IF EXISTS user;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
INSERT INTO users (email, password)
VALUES ("carlos@mail.com", "Admin1234");