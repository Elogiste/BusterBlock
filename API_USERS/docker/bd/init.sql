-- ===================================================================
--  Script SQL : Création et insertion des utilisateurs
--  Compatible : MariaDB / MySQL 10+
--  Encodage   : UTF-8
-- ===================================================================

-- (Optionnel) créer une base dédiée
CREATE DATABASE IF NOT EXISTS busterblock_utilisateurs CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'api'@'%' IDENTIFIED BY 'root';
GRANT ALL PRIVILEGES ON busterblock_utilisateurs.* TO 'api'@'%';
FLUSH PRIVILEGES;
USE busterblock_utilisateurs;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

SOURCE /docker-entrypoint-initdb.d/busterblock_utilisateurs.ldd;
SOURCE /docker-entrypoint-initdb.d/busterblock_utilisateurs.lmd;

SET FOREIGN_KEY_CHECKS = 1;

-- ===================================================================
-- Fin du script
-- ===================================================================
