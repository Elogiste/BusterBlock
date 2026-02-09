CREATE DATABASE IF NOT EXISTS busterblock_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'api'@'%' IDENTIFIED BY 'root';
GRANT ALL PRIVILEGES ON busterblock_test.* TO 'api'@'%';
---GRANT ALL PRIVILEGES ON busterblock_test.* TO 'root'@'%';---
FLUSH PRIVILEGES;

USE busterblock_test;

SOURCE /docker-entrypoint-initdb.d/busterblock.ldd;
SOURCE /docker-entrypoint-initdb.d/busterblock.lmd;
