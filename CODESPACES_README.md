# QualiSoja - GitHub Codespaces

Este guia te ajudará a configurar e executar o QualiSoja no GitHub Codespaces.

## 🚀 Início Rápido

### 1. Abrir no Codespaces
1. Vá para o repositório no GitHub
2. Clique no botão **Code** (verde)
3. Selecione a aba **Codespaces**
4. Clique em **Create codespace on main**

### 2. Aguardar Configuração Automática
O Codespace será configurado automaticamente com:
- ✅ Python 3.11
- ✅ Dependências instaladas
- ✅ Banco de dados configurado
- ✅ Superusuário criado (admin/admin123)
- ✅ Arquivos estáticos coletados

### 3. Iniciar o Servidor
```bash
# Ativar ambiente virtual
source venv/bin/activate

# Iniciar servidor Django
python manage.py runserver 0.0.0.0:8000
```

### 4. Acessar a Aplicação
- O VS Code mostrará uma notificação com o link
- Ou acesse: `https://SEU-CODESPACE-8000.app.github.dev`

## 🔧 Configurações Específicas do Codespaces

### Variáveis de Ambiente
O arquivo `.env` é criado automaticamente com:
```
DEBUG=True
SECRET_KEY=dev-secret-key-for-codespaces-only
ALLOWED_HOSTS=localhost,127.0.0.1,*.app.github.dev,*.preview.app.github.dev
CSRF_TRUSTED_ORIGINS=https://*.app.github.dev,https://*.preview.app.github.dev
```

### Arquivos Estáticos
- Os estilos CSS estão em `templates/static/geral/css/`
- Bootstrap 5 carregado via CDN
- Arquivos coletados automaticamente em `staticfiles/`

### Banco de Dados
- SQLite configurado automaticamente
- Migrações aplicadas na configuração inicial
- Superusuário: `admin` / `admin123`

## 🎨 Resolver Problemas de Estilos

Se os estilos não estiverem aparecendo:

### 1. Verificar Arquivos Estáticos
```bash
# Coletar arquivos estáticos novamente
python manage.py collectstatic --noinput

# Verificar se os arquivos existem
ls -la staticfiles/
ls -la templates/static/geral/css/
```

### 2. Verificar Configurações
```bash
# Verificar se DEBUG está ativo
python manage.py shell -c "from django.conf import settings; print(f'DEBUG: {settings.DEBUG}'); print(f'STATIC_URL: {settings.STATIC_URL}'); print(f'STATICFILES_DIRS: {settings.STATICFILES_DIRS}')"
```

### 3. Verificar no Browser
- Abra as **Ferramentas do Desenvolvedor** (F12)
- Vá na aba **Network**
- Recarregue a página
- Verifique se os arquivos CSS estão sendo carregados (status 200)

### 4. Forçar Reload
- `Ctrl+F5` ou `Cmd+Shift+R`
- Limpar cache do navegador

## 🐛 Troubleshooting

### Servidor não inicia
```bash
# Verificar se as dependências estão instaladas
pip list | grep Django

# Reinstalar dependências
pip install -r requirements.txt

# Verificar migrações
python manage.py showmigrations
python manage.py migrate
```

### Porta 8000 ocupada
```bash
# Usar porta diferente
python manage.py runserver 0.0.0.0:8080

# Ou encontrar processo que está usando a porta
lsof -i :8000
```

### Erro de CSRF
```bash
# Verificar CSRF_TRUSTED_ORIGINS
python manage.py shell -c "from django.conf import settings; print(settings.CSRF_TRUSTED_ORIGINS)"
```

## 📁 Estrutura do Projeto

```
qualisoja/
├── .devcontainer/          # Configuração do Codespaces
│   ├── devcontainer.json   # Configuração principal
│   └── setup.sh           # Script de configuração
├── .vscode/               # Configurações do VS Code
├── analises/              # App principal de análises
├── relatorios/            # App de relatórios
├── templates/             # Templates HTML e arquivos estáticos
│   └── static/geral/css/  # Arquivos CSS principais
├── staticfiles/           # Arquivos estáticos coletados
├── manage.py              # Django management
└── requirements.txt       # Dependências Python
```

## 🔗 Links Úteis

- **Admin**: `/admin/` (admin/admin123)
- **Análises**: `/analises/`
- **Relatórios**: `/relatorios/`
- **Health Check**: `/health/`

## 📞 Suporte

Se encontrar problemas:
1. Verifique este README
2. Consulte os logs: `tail -f qualisoja.log`
3. Recriar o Codespace se necessário

---
✨ **QualiSoja** - Sistema de Análises de Qualidade da Soja
