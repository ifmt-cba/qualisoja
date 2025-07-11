#!/bin/bash
set -e

echo "🚀 Iniciando QualiSoja - Ambiente de Produção"

# Verificar variáveis de ambiente obrigatórias
if [ -z "$SECRET_KEY" ]; then
    echo "❌ ERRO: SECRET_KEY não está definido"
    exit 1
fi

if [ -z "$ALLOWED_HOSTS" ]; then
    echo "❌ ERRO: ALLOWED_HOSTS não está definido"
    exit 1
fi

# Aguardar banco de dados (se usando PostgreSQL/MySQL)
if [ -n "$DATABASE_URL" ] || [ -n "$DB_HOST" ]; then
    echo "⏳ Aguardando banco de dados..."
    python << END
import os
import time
import django
from django.conf import settings
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

from django.db import connections
from django.db.utils import OperationalError

db = connections['default']
for i in range(30):
    try:
        db.cursor()
        print("✅ Banco de dados disponível!")
        break
    except OperationalError:
        print(f"⏳ Tentativa {i+1}/30 - Aguardando banco...")
        time.sleep(2)
else:
    print("❌ Banco de dados não disponível após 60 segundos")
    exit(1)
END
fi

# Executar migrações
echo "📦 Executando migrações..."
python manage.py migrate --noinput

# Coletar arquivos estáticos
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Verificar configuração do Django
echo "🔍 Verificando configuração..."
python manage.py check --deploy

# Criar superusuário se especificado
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "👤 Criando superusuário..."
    python manage.py shell << 'END'
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if not User.objects.filter(username=username).exists():
    try:
        User.objects.create_superuser(username, email, password)
        print(f'✅ Superusuário {username} criado com sucesso')
    except Exception as e:
        print(f'⚠️  Erro ao criar superusuário: {e}')
else:
    print(f'ℹ️  Superusuário {username} já existe')
END
fi

echo "✅ Inicialização de produção concluída!"
echo "🌐 Aplicação iniciando na porta 8000"

# Executar comando passado como parâmetro
exec "$@"
