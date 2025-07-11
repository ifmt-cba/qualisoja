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
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@qualisoja.com', 'admin123')
    print("✅ Superusuário criado: admin/admin123")
else:
    print("✅ Superusuário já existe")
END

echo "🎉 Ambiente de desenvolvimento pronto!"
echo "📍 Acesse: http://localhost:8000"
echo "👤 Admin: http://localhost:8000/admin (admin/admin123)"

# Executar comando passado como argumento
exec "$@"
