#!/bin/bash
# Script de Deploy para QualiSoja
# chmod +x deploy.sh

echo "🚀 Iniciando deploy do QualiSoja..."

# Parar serviços
echo "⏹️ Parando serviços..."
sudo systemctl stop gunicorn
sudo systemctl stop nginx

# Backup do banco de dados
echo "💾 Fazendo backup do banco..."
mkdir -p backups
cp db.sqlite3 backups/db_backup_$(date +%Y%m%d_%H%M%S).sqlite3

# Atualizar código
echo "📥 Atualizando código..."
git pull origin main

# Instalar dependências
echo "📦 Instalando dependências..."
pip install -r requirements.txt

# Coletar arquivos estáticos
echo "📄 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Aplicar migrações
echo "🗃️ Aplicando migrações..."
python manage.py migrate

# Verificar configurações
echo "✅ Verificando configurações..."
python manage.py check --deploy

# Reiniciar serviços
echo "🔄 Reiniciando serviços..."
sudo systemctl start gunicorn
sudo systemctl start nginx

# Verificar status
echo "📊 Status dos serviços:"
sudo systemctl status gunicorn --no-pager -l
sudo systemctl status nginx --no-pager -l

echo "✅ Deploy concluído!"
echo "🌐 Site disponível em: https://www.qualisoja.com.br"
