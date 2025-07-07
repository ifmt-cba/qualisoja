# 🔧 Ambiente de Desenvolvimento - QualiSoja

Este diretório contém as configurações Docker para o ambiente de desenvolvimento local.

## 📋 Pré-requisitos

- Docker Engine 20.10+
- Docker Compose 2.0+
- 4GB RAM disponível
- 2GB espaço em disco

## 🚀 Quick Start

### 1. Configurar variáveis de ambiente
```bash
# Copiar template de configuração
cp devops/templates/.env.example .env

# Editar configurações se necessário
vim .env
```

### 2. Subir o ambiente
```bash
# Entrar no diretório
cd devops/docker/development

# Subir todos os serviços
docker-compose up -d

# Verificar logs
docker-compose logs -f web
```

### 3. Acessar a aplicação
- **Aplicação:** http://localhost:8000
- **Admin Django:** http://localhost:8000/admin
  - Usuário: `admin`
  - Senha: `admin123`

## 🛠️ Serviços Disponíveis

| Serviço | URL | Descrição |
|---------|-----|-----------|
| Web App | http://localhost:8000 | Aplicação Django |
| PostgreSQL | localhost:5432 | Banco de dados |
| Redis | localhost:6379 | Cache e sessões |
| Adminer | http://localhost:8080 | Admin do banco |
| Redis Commander | http://localhost:8081 | Admin do Redis |

## 📊 Ferramentas de Desenvolvimento

### Acessar ferramentas de admin
```bash
# Subir ferramentas opcionais
docker-compose --profile tools up -d

# Adminer (DB Admin)
# http://localhost:8080
# Server: db
# User: postgres
# Password: postgres
# Database: qualisoja_dev

# Redis Commander
# http://localhost:8081
```

## 🔧 Comandos Úteis

### Gerenciar containers
```bash
# Subir serviços
docker-compose up -d

# Parar serviços
docker-compose down

# Rebuild containers
docker-compose up -d --build

# Ver logs
docker-compose logs -f [service_name]

# Executar comando no container
docker-compose exec web python manage.py shell
```

### Django management
```bash
# Migrações
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# Criar superusuário
docker-compose exec web python manage.py createsuperuser

# Coletar arquivos estáticos
docker-compose exec web python manage.py collectstatic

# Shell Django
docker-compose exec web python manage.py shell

# Tests
docker-compose exec web python manage.py test
```

### Banco de dados
```bash
# Backup
docker-compose exec db pg_dump -U postgres qualisoja_dev > backup.sql

# Restore
docker-compose exec -T db psql -U postgres qualisoja_dev < backup.sql

# Conectar ao banco
docker-compose exec db psql -U postgres qualisoja_dev
```

## 🗂️ Estrutura de Volumes

```
volumes/
├── postgres_data/     # Dados do PostgreSQL
├── redis_data/        # Dados do Redis
├── static_volume/     # Arquivos estáticos
└── media_volume/      # Arquivos de media
```

## 🐛 Troubleshooting

### Problemas Comuns

**Erro de permissão:**
```bash
# Resetar permissões
sudo chown -R $USER:$USER .
```

**Banco não conecta:**
```bash
# Verificar se o serviço está rodando
docker-compose ps

# Verificar logs do banco
docker-compose logs db
```

**Aplicação não carrega:**
```bash
# Verificar logs da aplicação
docker-compose logs web

# Rebuild do container
docker-compose up -d --build web
```

**Limpar tudo e recomeçar:**
```bash
# Parar e remover containers
docker-compose down -v

# Remover imagens
docker-compose down --rmi all

# Rebuild completo
docker-compose up -d --build
```

## 🔄 Hot Reload

O ambiente está configurado com hot reload:
- Mudanças no código Python são detectadas automaticamente
- Mudanças em templates são refletidas imediatamente
- Mudanças em arquivos estáticos requerem refresh do browser

## 📈 Performance

### Configurações otimizadas
- PostgreSQL com configurações de desenvolvimento
- Redis para cache de sessões
- Logging detalhado para debug
- Queries SQL logadas (> 1 segundo)

### Monitoramento
```bash
# Ver uso de recursos
docker stats

# Ver logs de performance
docker-compose logs web | grep "slow"
```

## 🔐 Segurança

- Usuário não-root no container
- Variáveis de ambiente para configurações sensíveis
- Rede isolada para os containers
- Volumes com permissões adequadas

---

**Última atualização:** Junho 2025
