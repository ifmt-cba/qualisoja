-- Script de inicialização do banco de dados para desenvolvimento
-- Este arquivo é executado automaticamente quando o container PostgreSQL é criado

-- Criar extensões úteis
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Criar usuário adicional para aplicação (opcional)
-- CREATE USER qualisoja_app WITH PASSWORD 'app_password';
-- GRANT ALL PRIVILEGES ON DATABASE qualisoja_dev TO qualisoja_app;

-- Configurações de performance para desenvolvimento
ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_statements';
ALTER SYSTEM SET pg_stat_statements.track = 'all';

-- Log de queries lentas (> 1 segundo)
ALTER SYSTEM SET log_min_duration_statement = 1000;
ALTER SYSTEM SET log_statement = 'all';

-- Recarregar configurações
SELECT pg_reload_conf();
