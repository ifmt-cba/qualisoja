#!/bin/bash
# Setup script para QualiSoja no Codespaces

echo "🚀 Configurando ambiente QualiSoja..."

# Atualizar sistema
sudo apt-get update

# Instalar dependências do sistema
sudo apt-get install -y \
    sqlite3 \
    postgresql-client \
    nginx \
    supervisor \
    gettext

# Criar ambiente virtual Python
echo "🐍 Configurando Python..."
python -m venv venv
source venv/bin/activate

# Instalar dependências Python
pip install --upgrade pip
pip install -r requirements.txt

# Configurar variáveis de ambiente para desenvolvimento
echo "⚙️ Configurando variáveis de ambiente..."
cat > .env << EOF
DEBUG=True
SECRET_KEY=dev-secret-key-for-codespaces-only
ALLOWED_HOSTS=localhost,127.0.0.1,*.app.github.dev,*.preview.app.github.dev
CSRF_TRUSTED_ORIGINS=https://*.app.github.dev,https://*.preview.app.github.dev,http://localhost:8000,http://127.0.0.1:8000
EOF

# Criar diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p staticfiles
mkdir -p media
mkdir -p logs

# Configurar banco de dados
echo "🗄️ Configurando banco de dados..."
python manage.py makemigrations
python manage.py migrate

# Criar superusuário (se não existir)
echo "👤 Verificando superusuário..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@qualisoja.com', 'admin123')
    print('Superusuário criado: admin/admin123')
else:
    print('Superusuário já existe')
EOF

# Coletar arquivos estáticos
echo "📄 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Configurar permissões
chmod +x manage.py
chmod -R 755 staticfiles/

echo "✅ Configuração concluída!"
echo "🌐 Para iniciar o servidor: python manage.py runserver 0.0.0.0:8000"
echo "👤 Admin: admin / admin123"
