#!/bin/bash
set -e

echo "🚀 Iniciando QualiSoja - Ambiente de Desenvolvimento"

# Aguardar um momento para estabilizar
sleep 2

# Executar migrações
echo "📦 Executando migrações..."
python manage.py migrate --noinput

# Coletar arquivos estáticos
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Criar superusuário se não existir
echo "👤 Verificando superusuário..."
python manage.py shell << 'END'
from django.contrib.auth import get_user_model
try:
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        user = User.objects.create_superuser('admin', 'admin@qualisoja.com', 'admin123')
        print('✅ Superusuário criado: admin/admin123')
    else:
        print('ℹ️  Superusuário já existe')
except Exception as e:
    print(f'⚠️  Erro ao criar superusuário: {e}')
    print('ℹ️  Continuando com a inicialização...')
END

echo "✅ Inicialização concluída!"
echo "🌐 Aplicação disponível em: http://localhost:8000"
echo "🔧 Admin disponível em: http://localhost:8000/admin"

# Executar comando passado como parâmetro
exec "$@"
