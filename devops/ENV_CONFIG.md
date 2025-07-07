# 🔐 Configurações de Ambiente - QualiSoja DevOps

## 📋 Variáveis de Ambiente por Ambiente

### 🔧 Development
```bash
# Django
DEBUG=True
SECRET_KEY=dev-secret-key-change-me
DJANGO_SETTINGS_MODULE=qualisoja.settings.development

# Database
DATABASE_URL=sqlite:///db.sqlite3
# Ou para PostgreSQL local:
# DATABASE_URL=postgresql://postgres:postgres@localhost:5432/qualisoja_dev

# Cache
REDIS_URL=redis://localhost:6379/0

# Media/Static
MEDIA_ROOT=/app/media
STATIC_ROOT=/app/static

# Email (desenvolvimento)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Logging
LOG_LEVEL=DEBUG
```

### 🧪 Testing
```bash
# Django
DEBUG=False
SECRET_KEY=test-secret-key
DJANGO_SETTINGS_MODULE=qualisoja.settings.testing

# Database (in-memory)
DATABASE_URL=sqlite://:memory:

# Cache
REDIS_URL=redis://localhost:6379/1

# Testing specific
TEST_MODE=True
COVERAGE_REPORT=True
```

### 🚀 Production
```bash
# Django
DEBUG=False
SECRET_KEY=${SECRET_KEY}
DJANGO_SETTINGS_MODULE=qualisoja.settings.production
ALLOWED_HOSTS=qualisoja.com,www.qualisoja.com

# Database
DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:5432/${DB_NAME}

# Cache
REDIS_URL=redis://${REDIS_HOST}:6379/0

# Security
SSL_REDIRECT=True
SECURE_PROXY_SSL_HEADER=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Media/Static
MEDIA_ROOT=/app/media
STATIC_ROOT=/app/static
AWS_STORAGE_BUCKET_NAME=${S3_BUCKET}  # Se usar S3

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=${SMTP_HOST}
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=${SMTP_USER}
EMAIL_HOST_PASSWORD=${SMTP_PASSWORD}

# Monitoring
SENTRY_DSN=${SENTRY_DSN}

# Logging
LOG_LEVEL=INFO
```

## 🔒 Secrets Management

### Desenvolvimento Local
Criar arquivo `.env` na raiz do projeto:
```bash
cp devops/templates/.env.example .env
```

### Kubernetes Secrets
```bash
# Criar secrets no cluster
kubectl create secret generic qualisoja-secrets \
  --from-literal=secret-key=${SECRET_KEY} \
  --from-literal=database-url=${DATABASE_URL} \
  --from-literal=redis-url=${REDIS_URL}
```

### GitHub Secrets
Configurar no repositório GitHub:
- `SECRET_KEY`
- `DATABASE_URL`  
- `REDIS_URL`
- `DOCKER_REGISTRY_TOKEN`
- `KUBECONFIG`

## 📁 Arquivos de Template

### .env.example
```bash
# Copie para .env e preencha os valores
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://localhost:6379/0
```

### .env.production.example
```bash
DEBUG=False
SECRET_KEY=
DATABASE_URL=
REDIS_URL=
ALLOWED_HOSTS=
SENTRY_DSN=
```

## 🛡️ Boas Práticas de Segurança

1. **Nunca committar secrets** no código
2. **Usar diferentes keys** por ambiente
3. **Rotacionar secrets** regularmente
4. **Minimal permissions** para cada ambiente
5. **Audit logs** para acesso a secrets

## 🔄 Rotação de Secrets

### Trimestral
- SECRET_KEY
- Database passwords
- API tokens

### Anual
- SSL certificates
- Service account keys

---

**⚠️ IMPORTANTE:** Nunca compartilhe secrets em canais inseguros!
