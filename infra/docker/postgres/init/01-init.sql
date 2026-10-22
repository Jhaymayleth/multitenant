-- -----------------------------------------------------------------------------
-- Lixus — Inicialización de PostgreSQL
-- -----------------------------------------------------------------------------
-- Basado en docs/03-ARQUITECTURA.md (Sección 2.5) y docs/07-MODELO-DATOS.md
-- -----------------------------------------------------------------------------

-- 1. Extensiones requeridas
CREATE EXTENSION IF NOT EXISTS "citext";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "btree_gist";

-- 2. Schema global de la plataforma
CREATE SCHEMA IF NOT EXISTS platform;

-- 3. Roles de base de datos para cumplimiento de seguridad
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'lixus_migrator') THEN
        CREATE ROLE lixus_migrator WITH LOGIN PASSWORD 'migrator_secret_local';
    END IF;
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'lixus_app') THEN
        CREATE ROLE lixus_app WITH LOGIN PASSWORD 'app_secret_local';
    END IF;
END
$$;

-- Permisos básicos iniciales para desarrollo local
GRANT ALL PRIVILEGES ON SCHEMA platform TO lixus;
GRANT ALL PRIVILEGES ON SCHEMA public TO lixus;

