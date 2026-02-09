-- ===================================================================
--  Script SQL : Création et insertion des magasins et films
--  Compatible : MariaDB / MySQL 10+
--  Encodage   : UTF-8
-- ===================================================================

-- (Optionnel) créer une base dédiée
CREATE DATABASE IF NOT EXISTS busterblock_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

GRANT ALL PRIVILEGES ON busterblock_db.* TO 'root'@'%';
FLUSH PRIVILEGES;

USE busterblock_db;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

SOURCE /docker-entrypoint-initdb.d/busterblock.ldd;
SOURCE /docker-entrypoint-initdb.d/busterblock.lmd;

SET FOREIGN_KEY_CHECKS = 1;

-- ===================================================================
-- Fin du script
-- ===================================================================
