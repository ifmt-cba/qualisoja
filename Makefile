# Makefile para automação de comandos DevOps - QualiSoja
.PHONY: help dev prod test clean logs shell migrate backup

# Cores para output
RED=\033[0;31m
GREEN=\033[0;32m
YELLOW=\033[1;33m
BLUE=\033[0;34m
NC=\033[0m # No Color

# Variáveis
DOCKER_COMPOSE_DEV=devops/docker/development/docker-compose-simple.yml
DOCKER_COMPOSE_FULL=devops/docker/development/docker-compose.yml
DOCKER_COMPOSE_PROD=devops/docker/production/docker-compose.yml
DOCKER_COMPOSE_TEST=devops/docker/testing/docker-compose.yml

help: ## Mostrar ajuda
	@echo "$(BLUE)🚀 QualiSoja DevOps Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

# Comandos de Desenvolvimento
dev-up: ## Subir ambiente de desenvolvimento
	@echo "$(YELLOW)🔧 Subindo ambiente de desenvolvimento...$(NC)"
	docker-compose -f $(DOCKER_COMPOSE_DEV) up -d
	@echo "$(GREEN)✅ Ambiente disponível em http://localhost:8000$(NC)"

dev-down: ## Parar ambiente de desenvolvimento
	@echo "$(YELLOW)🛑 Parando ambiente de desenvolvimento...$(NC)"
	docker-compose -f $(DOCKER_COMPOSE_DEV) down

dev-build: ## Rebuild ambiente de desenvolvimento
	@echo "$(YELLOW)🔨 Rebuilding ambiente de desenvolvimento...$(NC)"
	docker-compose -f $(DOCKER_COMPOSE_DEV) up -d --build

dev-logs: ## Ver logs do ambiente de desenvolvimento
	docker-compose -f $(DOCKER_COMPOSE_DEV) logs -f

dev-shell: ## Acessar shell da aplicação
	docker-compose -f $(DOCKER_COMPOSE_DEV) exec web bash

dev-django: ## Acessar Django shell
	docker-compose -f $(DOCKER_COMPOSE_DEV) exec web python manage.py shell

dev-tools: ## Subir ferramentas de desenvolvimento (Adminer, Redis Commander)
	@echo "$(YELLOW)🛠️ Subindo ferramentas de desenvolvimento...$(NC)"
	docker-compose -f $(DOCKER_COMPOSE_DEV) --profile tools up -d
	@echo "$(GREEN)📊 Adminer: http://localhost:8080$(NC)"
	@echo "$(GREEN)📊 Redis Commander: http://localhost:8081$(NC)"

# Comandos Django
migrate: ## Executar migrações
	@echo "$(YELLOW)📦 Executando migrações...$(NC)"
	docker-compose -f $(DOCKER_COMPOSE_DEV) exec web python manage.py migrate

makemigrations: ## Criar migrações
	@echo "$(YELLOW)📦 Criando migrações...$(NC)"
	docker-compose -f $(DOCKER_COMPOSE_DEV) exec web python manage.py makemigrations

collectstatic: ## Coletar arquivos estáticos
	@echo "$(YELLOW)📁 Coletando arquivos estáticos...$(NC)"
	docker-compose -f $(DOCKER_COMPOSE_DEV) exec web python manage.py collectstatic --noinput

superuser: ## Criar superusuário
	@echo "$(YELLOW)👤 Criando superusuário...$(NC)"
	docker-compose -f $(DOCKER_COMPOSE_DEV) exec web python manage.py createsuperuser

# Comandos de Teste
test: ## Executar testes
	@echo "$(YELLOW)🧪 Executando testes...$(NC)"
	docker-compose -f $(DOCKER_COMPOSE_DEV) exec web python manage.py test

test-coverage: ## Executar testes com coverage
	@echo "$(YELLOW)🧪 Executando testes com coverage...$(NC)"
	docker-compose -f $(DOCKER_COMPOSE_DEV) exec web coverage run --source='.' manage.py test
	docker-compose -f $(DOCKER_COMPOSE_DEV) exec web coverage report
	docker-compose -f $(DOCKER_COMPOSE_DEV) exec web coverage html

# Comandos de Banco de Dados
db-backup: ## Fazer backup do banco
	@echo "$(YELLOW)💾 Fazendo backup do banco...$(NC)"
	docker-compose -f $(DOCKER_COMPOSE_DEV) exec db pg_dump -U postgres qualisoja_dev > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)✅ Backup criado!$(NC)"

db-restore: ## Restaurar backup do banco (usar: make db-restore FILE=backup.sql)
	@echo "$(YELLOW)🔄 Restaurando backup do banco...$(NC)"
	docker-compose -f $(DOCKER_COMPOSE_DEV) exec -T db psql -U postgres qualisoja_dev < $(FILE)
	@echo "$(GREEN)✅ Backup restaurado!$(NC)"

db-shell: ## Acessar shell do PostgreSQL
	docker-compose -f $(DOCKER_COMPOSE_DEV) exec db psql -U postgres qualisoja_dev

# Comandos de Limpeza
clean: ## Limpar containers, volumes e imagens
	@echo "$(RED)🧹 Limpando ambiente...$(NC)"
	docker-compose -f $(DOCKER_COMPOSE_DEV) down -v
	docker system prune -f
	@echo "$(GREEN)✅ Ambiente limpo!$(NC)"

clean-all: ## Limpar tudo (incluindo imagens)
	@echo "$(RED)🧹 Limpeza completa...$(NC)"
	docker-compose -f $(DOCKER_COMPOSE_DEV) down -v --rmi all
	docker system prune -af
	@echo "$(GREEN)✅ Limpeza completa realizada!$(NC)"

# Comandos de Produção
prod-up: ## Subir ambiente de produção
	@echo "$(YELLOW)🚀 Subindo ambiente de produção...$(NC)"
	docker-compose -f $(DOCKER_COMPOSE_PROD) up -d
	@echo "$(GREEN)✅ Ambiente de produção disponível!$(NC)"

prod-down: ## Parar ambiente de produção
	@echo "$(YELLOW)🛑 Parando ambiente de produção...$(NC)"
	docker-compose -f $(DOCKER_COMPOSE_PROD) down

prod-logs: ## Ver logs do ambiente de produção
	docker-compose -f $(DOCKER_COMPOSE_PROD) logs -f

# 🚀 DOCKER PRODUCTION
.PHONY: docker-build-prod docker-run-prod docker-push
docker-build-prod: ## Build imagem de produção
	@echo "🔨 Building production Docker image..."
	docker build -f devops/docker/production/Dockerfile -t qualisoja:production .

docker-run-prod: ## Executar stack de produção
	@echo "🚀 Starting production stack..."
	cd devops/docker/production && docker-compose up -d

docker-push: ## Push imagem para registry
	@echo "📤 Pushing image to registry..."
	docker tag qualisoja:production ghcr.io/qualisoja/qualisoja:latest
	docker push ghcr.io/qualisoja/qualisoja:latest

# 🔄 CI/CD
.PHONY: lint security-scan performance-test
lint: ## Análise de qualidade do código
	@echo "🔍 Running code quality checks..."
	python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	python -m black --check --diff .
	python -m isort --check-only --diff .

security-scan: ## Verificação de segurança
	@echo "🔒 Running security scans..."
	python -m bandit -r . -x tests/
	python -m safety check

performance-test: ## Testes de performance
	@echo "⚡ Running performance tests..."
	python -m locust --headless --users 10 --spawn-rate 2 --run-time 30s --host=http://localhost:8000

# 📊 MONITORING
.PHONY: health-check metrics
health-check: ## Verificar saúde da aplicação
	@echo "❤️ Checking application health..."
	curl -f http://localhost:8000/health/ || echo "Health check failed"

metrics: ## Ver métricas do container
	@echo "📊 Container metrics:"
	docker stats --no-stream qualisoja-dev 2>/dev/null || echo "Container not running"

# Comandos de Monitoramento
status: ## Verificar status dos containers
	@echo "$(BLUE)📊 Status dos containers:$(NC)"
	docker-compose -f $(DOCKER_COMPOSE_DEV) ps

logs: ## Ver logs de todos os serviços
	docker-compose -f $(DOCKER_COMPOSE_DEV) logs --tail=50

logs-web: ## Ver logs apenas da aplicação web
	docker-compose -f $(DOCKER_COMPOSE_DEV) logs -f web

logs-db: ## Ver logs apenas do banco de dados
	docker-compose -f $(DOCKER_COMPOSE_DEV) logs -f db

# Comandos de Instalação
install: ## Instalar dependências
	@echo "$(YELLOW)📦 Instalando dependências...$(NC)"
	docker-compose -f $(DOCKER_COMPOSE_DEV) exec web pip install -r requirements.txt

requirements: ## Atualizar requirements.txt
	@echo "$(YELLOW)📦 Atualizando requirements.txt...$(NC)"
	docker-compose -f $(DOCKER_COMPOSE_DEV) exec web pip freeze > requirements.txt

# Comandos de Qualidade de Código
lint: ## Executar linting
	@echo "$(YELLOW)🔍 Executando linting...$(NC)"
	docker-compose -f $(DOCKER_COMPOSE_DEV) exec web flake8 .

format: ## Formatar código
	@echo "$(YELLOW)✨ Formatando código...$(NC)"
	docker-compose -f $(DOCKER_COMPOSE_DEV) exec web black .

# Comandos de Inicialização
init: dev-up migrate collectstatic superuser ## Inicialização completa do ambiente
	@echo "$(GREEN)🎉 Ambiente inicializado com sucesso!$(NC)"
	@echo "$(GREEN)🌐 Acesse: http://localhost:8000$(NC)"
	@echo "$(GREEN)👤 Admin: http://localhost:8000/admin$(NC)"

# Comandos de Informação
info: ## Mostrar informações do ambiente
	@echo "$(BLUE)ℹ️ Informações do Ambiente:$(NC)"
	@echo "$(GREEN)🌐 Aplicação: http://localhost:8000$(NC)"
	@echo "$(GREEN)👤 Admin: http://localhost:8000/admin$(NC)"
	@echo "$(GREEN)📊 Adminer: http://localhost:8080$(NC)"
	@echo "$(GREEN)📊 Redis Commander: http://localhost:8081$(NC)"
	@echo "$(GREEN)🗄️ PostgreSQL: localhost:5432$(NC)"
	@echo "$(GREEN)🗃️ Redis: localhost:6379$(NC)"

# ☸️ KUBERNETES
.PHONY: k8s-deploy-manifests k8s-deploy-helm k8s-status k8s-logs k8s-cleanup k8s-port-forward
k8s-deploy-manifests: ## Deploy usando manifests Kubernetes
	@echo "☸️ Deploying with Kubernetes manifests..."
	./devops/scripts/k8s-deploy.sh deploy-manifests

k8s-deploy-helm: ## Deploy usando Helm Chart
	@echo "⚓ Deploying with Helm..."
	./devops/scripts/k8s-deploy.sh deploy-helm

k8s-status: ## Verificar status do deployment K8s
	@echo "📊 Checking Kubernetes deployment status..."
	./devops/scripts/k8s-deploy.sh status

k8s-logs: ## Ver logs da aplicação no K8s
	@echo "📋 Showing application logs..."
	./devops/scripts/k8s-deploy.sh logs

k8s-port-forward: ## Port forward para acesso local (porta 8000)
	@echo "🔗 Starting port forward to localhost:8000..."
	./devops/scripts/k8s-deploy.sh port-forward

k8s-cleanup: ## Remover recursos do Kubernetes
	@echo "🧹 Cleaning up Kubernetes resources..."
	./devops/scripts/k8s-deploy.sh cleanup
